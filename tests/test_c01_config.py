"""
單元測試：CARD-01 系統環境配置與 Gemini API 金鑰池管理
遵循 80% 簡化技術中文規範 (STE-TW)
"""
import os
import pytest
from src.c01_config import Config, KeyPoolManager


def test_key_pool_parsing():
    """驗證多金鑰字串正確解析為清單"""
    raw_keys = "key_alpha, key_beta,key_gamma"
    pool = KeyPoolManager(raw_keys)
    assert pool.keys == ["key_alpha", "key_beta", "key_gamma"]
    assert len(pool.keys) == 3


def test_key_pool_round_robin():
    """驗證金鑰輪詢機制依序取用"""
    pool = KeyPoolManager(["key_1", "key_2", "key_3"])
    assert pool.get_next_key() == "key_1"
    assert pool.get_next_key() == "key_2"
    assert pool.get_next_key() == "key_3"
    # 第四次取用回到第一組
    assert pool.get_next_key() == "key_1"


def test_key_pool_rate_limited_switch():
    """驗證金鑰遭遇限流時自動切換至下一組可用金鑰"""
    pool = KeyPoolManager(["key_A", "key_B"])
    assert pool.get_next_key() == "key_A"
    
    # 標記 key_A 限流
    pool.mark_key_rate_limited("key_A", cooldown_seconds=60)
    
    # 下一次取用必須直接跳過 key_A，取得 key_B
    assert pool.get_next_key() == "key_B"
    # 再次取用仍為 key_B（因為 key_A 冷卻中）
    assert pool.get_next_key() == "key_B"


def test_config_env_loading(monkeypatch):
    """驗證 Config 類別正確自環境變數載入參數"""
    monkeypatch.setenv("GEMINI_API_KEYS", "k1,k2")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "mock_bot_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "mock_chat_id")
    
    config = Config.from_env()
    assert config.gemini_keys == ["k1", "k2"]
    assert config.telegram_bot_token == "mock_bot_token"
    assert config.telegram_chat_id == "mock_chat_id"
    assert len(config.tw_universe) > 0
    assert len(config.us_universe) > 0
