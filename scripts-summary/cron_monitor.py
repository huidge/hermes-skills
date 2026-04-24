#!/usr/bin/env python3
"""
Cron Job Monitor - 监控定时任务执行状态并发送告警
"""
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# 添加 hermes 模块路径
sys.path.insert(0, str(Path.home() / '.hermes' / 'hermes-agent'))

def load_cron_jobs():
    """加载 cron 任务配置"""
    jobs_file = Path.home() / '.hermes' / 'cron_jobs.json'
    if not jobs_file.exists():
        return {}
    
    try:
        with open(jobs_file, 'r') as f:
            data = json.load(f)
            return data.get('jobs', {})
    except Exception as e:
        print(f"Error loading cron jobs: {e}")
        return {}

def check_job_status(job_id, job_config):
    """检查单个任务的状态"""
    # 获取上次运行时间
    last_run_at = job_config.get('last_run_at')
    last_status = job_config.get('last_status')
    schedule = job_config.get('schedule', '')
    
    if not last_run_at:
        # 从未运行过
        return {
            'job_id': job_id,
            'name': job_config.get('name', 'Unknown'),
            'status': 'never_run',
            'message': '任务从未运行过'
        }
    
    # 解析上次运行时间
    try:
        last_run_time = datetime.fromisoformat(last_run_at.replace('Z', '+00:00'))
        now = datetime.now(last_run_time.tzinfo)
        
        # 检查是否应该运行但没有成功运行
        if last_status != 'ok':
            return {
                'job_id': job_id,
                'name': job_config.get('name', 'Unknown'),
                'status': 'failed',
                'last_run': last_run_at,
                'last_status': last_status,
                'message': f'上次运行失败: {last_status}'
            }
        
        # 检查是否长时间未运行（根据调度频率判断）
        # 这里简化处理，如果超过24小时没运行就告警
        time_since_last_run = now - last_run_time
        if time_since_last_run > timedelta(hours=24):
            return {
                'job_id': job_id,
                'name': job_config.get('name', 'Unknown'),
                'status': 'stale',
                'last_run': last_run_at,
                'hours_since': time_since_last_run.total_seconds() / 3600,
                'message': f'任务已 {time_since_last_run.total_seconds() / 3600:.1f} 小时未运行'
            }
        
        return {
            'job_id': job_id,
            'name': job_config.get('name', 'Unknown'),
            'status': 'ok',
            'last_run': last_run_at,
            'message': '正常'
        }
    
    except Exception as e:
        return {
            'job_id': job_id,
            'name': job_config.get('name', 'Unknown'),
            'status': 'error',
            'message': f'解析状态失败: {e}'
        }

def send_wechat_alert(alert_message):
    """通过微信发送告警"""
    try:
        # 这里简化处理，实际应该调用 hermes 的 API
        # 或者直接调用微信 API
        print(f"[ALERT] {alert_message}")
        return True
    except Exception as e:
        print(f"Failed to send alert: {e}")
        return False

def main():
    """主函数"""
    print(f"Starting cron job monitor at {datetime.now()}")
    
    # 加载任务配置
    jobs = load_cron_jobs()
    if not jobs:
        print("No cron jobs found")
        return
    
    alerts = []
    
    # 检查每个任务的状态
    for job_id, job_config in jobs.items():
        status = check_job_status(job_id, job_config)
        
        if status['status'] != 'ok':
            alerts.append(status)
    
    # 如果有告警，发送通知
    if alerts:
        alert_message = "🚨 定时任务告警:\n\n"
        for alert in alerts:
            alert_message += f"• {alert['name']}: {alert['message']}\n"
        
        send_wechat_alert(alert_message)
        print(f"Found {len(alerts)} alerts")
    else:
        print("All jobs are running normally")

if __name__ == '__main__':
    main()
