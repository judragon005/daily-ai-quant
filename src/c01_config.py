"""
CARD-01 系統環境配置與 API 金鑰池管理模組
遵循 80% 簡化技術中文規範 (STE-TW)
"""
import os
import time
from typing import List, Optional


class KeyPoolManager:
    """管理 Gemini API 金鑰輪詢與冷卻機制"""

    def __init__(self, keys: str | List[str]):
        if isinstance(keys, str):
            # 以逗號切割並清除前後空格
            self.keys = [k.strip() for k in keys.split(",") if k.strip()]
        else:
            self.keys = [k.strip() for k in keys if k.strip()]
        
        self._current_index = 0
        self._cooldowns: dict[str, float] = {}

    def get_next_key(self) -> str:
        """輪詢取得下一組可用金鑰。若全部冷卻則回傳最早過期者"""
        if not self.keys:
            raise ValueError("金鑰池為空，請配置有效 API 金鑰。")

        now = time.time()
        # 尋找未在冷卻期內的金鑰
        for _ in range(len(self.keys)):
            key = self.keys[self._current_index]
            self._current_index = (self._current_index + 1) % len(self.keys)
            
            # 檢查冷卻時間是否已結束
            cooldown_until = self._cooldowns.get(key, 0)
            if now >= cooldown_until:
                return key

        # 若全部金鑰都在冷卻中，選取剩餘冷卻時間最短的金鑰
        return min(self.keys, key=lambda k: self._cooldowns.get(k, 0))

    def mark_key_rate_limited(self, key: str, cooldown_seconds: int = 60) -> None:
        """標記指定金鑰進入冷卻狀態"""
        self._cooldowns[key] = time.time() + cooldown_seconds


class Config:
    """系統設定資料類別"""

    def __init__(
        self,
        gemini_keys: List[str],
        telegram_bot_token: str = "",
        telegram_chat_id: str = "",
        tw_universe: Optional[List[str]] = None,
        us_universe: Optional[List[str]] = None,
    ):
        self.gemini_keys = gemini_keys
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id
        
        # 台股母池預設標的 (臺灣 50 與核心流動標的)
        self.tw_universe = tw_universe or [
            "2330.TW", "2317.TW", "2454.TW", "2382.TW", "2308.TW",
            "2881.TW", "2882.TW", "2412.TW", "2891.TW", "3711.TW",
            "3008.TW", "2357.TW", "2603.TW", "2327.TW", "3231.TW",
            "2379.TW", "2886.TW", "6505.TW", "4938.TW", "2884.TW",
        ]
        
        # 美股母池預設標的 (S&P 500 與科技權值)
        self.us_universe = us_universe or [
            "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL",
            "META", "TSLA", "AVGO", "COST", "AMD",
            "NFLX", "PLTR", "TXN", "QCOM", "INTC",
            "CRM", "IBM", "AMAT", "MU", "PANW",
        ]

    @classmethod
    def from_env(cls) -> "Config":
        """自系統環境變數建立設定實例"""
        raw_keys = os.getenv("GEMINI_API_KEYS", "")
        keys = [k.strip() for k in raw_keys.split(",") if k.strip()]
        
        return cls(
            gemini_keys=keys,
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
        )
