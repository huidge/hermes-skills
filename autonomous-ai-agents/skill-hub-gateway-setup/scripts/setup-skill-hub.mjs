#!/usr/bin/env node
/**
 * Skill Hub Gateway 配置脚本
 * 自动获取 API key 并配置认证
 */

import os from 'os';
import crypto from 'crypto';
import path from 'path';

const DEFAULT_BASE_URL = 'https://gateway-api.binaryworks.app';

async function postJson(baseUrl, path, body) {
  const response = await fetch(`${baseUrl}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });

  const text = await response.text();
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    parsed = null;
  }

  return {
    ok: response.ok,
    status: response.status,
    text,
    parsed
  };
}

async function issueInstallCode(baseUrl, ownerUidHint) {
  console.log('📋 正在获取 install code...');
  
  const response = await postJson(baseUrl, '/agent/install-code/issue', {
    channel: 'local',
    owner_uid_hint: ownerUidHint
  });

  if (!response.ok || !response.parsed) {
    throw new Error(`获取 install code 失败: ${response.status} ${response.text}`);
  }

  const data = response.parsed.data;
  if (!data || !data.install_code) {
    throw new Error('响应中缺少 install_code');
  }

  console.log('✅ Install code 获取成功');
  return {
    installCode: data.install_code,
    ownerUid: data.owner_uid
  };
}

async function bootstrapAgent(baseUrl, installCode, agentUid) {
  console.log('🔐 正在引导 agent 认证...');
  
  const response = await postJson(baseUrl, '/agent/bootstrap', {
    agent_uid: agentUid,
    install_code: installCode
  });

  if (!response.ok || !response.parsed) {
    throw new Error(`引导 agent 失败: ${response.status} ${response.text}`);
  }

  const data = response.parsed.data;
  if (!data || !data.api_key) {
    throw new Error('响应中缺少 api_key');
  }

  console.log('✅ API key 获取成功');
  return {
    apiKey: data.api_key,
    ownerUid: data.owner_uid
  };
}

async function testApiKey(baseUrl, apiKey) {
  console.log('🧪 正在测试 API key...');
  
  const response = await fetch(`${baseUrl}/skills/manifest.json`, {
    method: 'GET',
    headers: {
      'X-API-Key': apiKey
    }
  });

  if (response.ok) {
    console.log('✅ API key 测试成功');
    return true;
  } else {
    console.log(`⚠️  API key 测试返回: ${response.status}`);
    return false;
  }
}

function generateAgentUid() {
  // 生成一个稳定的 agent_uid - 格式: agent_[a-z0-9][a-z0-9_-]{5,63}
  const homeDir = os.homedir();
  const workspacePath = path.join(homeDir, '.openclaw', 'workspace');
  const hash = crypto.createHash('sha256')
    .update(`agent:${workspacePath}`)
    .digest('hex')
    .slice(0, 24);
  
  return `agent_${hash}`;
}

function generateOwnerUid() {
  // 生成一个稳定的 owner_uid - 格式: owner_[a-z0-9][a-z0-9_-]{5,63}
  const homeDir = os.homedir();
  const workspacePath = path.join(homeDir, '.openclaw', 'workspace');
  const hash = crypto.createHash('sha256')
    .update(`owner:${workspacePath}`)
    .digest('hex')
    .slice(0, 24);
  
  return `owner_${hash}`;
}

async function main() {
  console.log('🚀 Skill Hub Gateway 配置向导');
  console.log('================================\n');

  const baseUrl = process.env.SKILL_HUB_BASE_URL || DEFAULT_BASE_URL;
  console.log(`📡 API 地址: ${baseUrl}\n`);

  try {
    // 生成 agent_uid 和 owner_uid
    const agentUid = generateAgentUid();
    const ownerUidHint = generateOwnerUid();
    console.log(`🆔 Agent UID: ${agentUid}`);
    console.log(`👤 Owner UID Hint: ${ownerUidHint}\n`);

    // 获取 install code
    const { installCode, ownerUid } = await issueInstallCode(baseUrl, ownerUidHint);
    console.log(`✅ Owner UID: ${ownerUid}\n`);

    // 引导 agent
    const { apiKey } = await bootstrapAgent(baseUrl, installCode, agentUid);

    // 测试 API key
    await testApiKey(baseUrl, apiKey);

    // 输出配置信息
    console.log('\n================================');
    console.log('🎉 配置完成！');
    console.log('================================\n');
    console.log('请将以下配置添加到 ~/.hermes/.env 文件:\n');
    console.log(`SKILL_HUB_API_KEY=${apiKey}`);
    console.log(`SKILL_HUB_AGENT_UID=${agentUid}`);
    console.log(`SKILL_HUB_OWNER_UID=${ownerUid}`);
    console.log(`SKILL_HUB_BASE_URL=${baseUrl}`);

  } catch (error) {
    console.error('\n❌ 配置失败:', error.message);
    process.exit(1);
  }
}

main();
