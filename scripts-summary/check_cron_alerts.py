#!/usr/bin/env python3
"""
简单的定时任务监控脚本
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def parse_cron_output(output):
    """解析 hermes cron list 的输出"""
    jobs = []
    lines = output.split('\n')
    current_job = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 检测任务 ID 行
        if '[active]' in line or '[paused]' in line:
            if current_job:
                jobs.append(current_job)
            
            # 解析任务 ID 和状态
            parts = line.split()
            job_id = parts[0]
            status = 'active' if '[active]' in line else 'paused'
            
            current_job = {
                'job_id': job_id,
                'status': status
            }
        
        # 解析其他字段
        elif current_job:
            if line.startswith('Name:'):
                current_job['name'] = line[5:].strip()
            elif line.startswith('Schedule:'):
                current_job['schedule'] = line[9:].strip()
            elif line.startswith('Next run:'):
                current_job['next_run'] = line[9:].strip()
            elif line.startswith('Last run:'):
                last_run_part = line[9:].strip()
                # 解析 "2026-04-16T22:42:46.674699+08:00  ok" 格式
                if '  ' in last_run_part:
                    time_part, status_part = last_run_part.split('  ', 1)
                    current_job['last_run_at'] = time_part
                    current_job['last_status'] = status_part.strip()
                else:
                    current_job['last_run_at'] = last_run_part
                    current_job['last_status'] = 'unknown'
            elif line.startswith('Deliver:'):
                current_job['deliver'] = line[8:].strip()
    
    # 添加最后一个任务
    if current_job:
        jobs.append(current_job)
    
    return jobs

def get_cron_jobs():
    """获取所有定时任务"""
    try:
        # 使用 hermes 命令获取任务列表
        result = subprocess.run(
            ['hermes', 'cron', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return parse_cron_output(result.stdout)
        else:
            print(f"Error getting cron jobs: {result.stderr}")
            return []
    except Exception as e:
        print(f"Exception: {e}")
        return []

def check_job_alerts():
    """检查任务告警"""
    jobs = get_cron_jobs()
    if not jobs:
        print("No jobs found")
        return []
    
    alerts = []
    
    for job in jobs:
        job_id = job.get('job_id')
        name = job.get('name', 'Unknown')
        last_run_at = job.get('last_run_at')
        last_status = job.get('last_status')
        
        # 检查任务状态
        if not last_run_at:
            alerts.append({
                'job_id': job_id,
                'name': name,
                'type': 'never_run',
                'message': f'任务 "{name}" 从未运行过'
            })
        elif last_status and last_status != 'ok':
            alerts.append({
                'job_id': job_id,
                'name': name,
                'type': 'failed',
                'last_run': last_run_at,
                'status': last_status,
                'message': f'任务 "{name}" 上次运行失败: {last_status}'
            })
    
    return alerts

def main():
    """主函数"""
    print(f"Checking cron jobs at {datetime.now()}")
    
    alerts = check_job_alerts()
    
    if alerts:
        print(f"Found {len(alerts)} alerts:")
        for alert in alerts:
            print(f"  - {alert['message']}")
        
        # 这里可以添加发送告警的逻辑
        # 例如通过微信、邮件等
        alert_message = "🚨 定时任务告警:\n\n"
        for alert in alerts:
            alert_message += f"• {alert['message']}\n"
        
        print("\nAlert message:")
        print(alert_message)
        
        # 保存告警记录
        alert_file = Path.home() / '.hermes' / 'logs' / f'alert_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        alert_file.parent.mkdir(parents=True, exist_ok=True)
        with open(alert_file, 'w') as f:
            f.write(alert_message)
        
        print(f"Alert saved to: {alert_file}")
    else:
        print("All jobs are running normally")

if __name__ == '__main__':
    main()
