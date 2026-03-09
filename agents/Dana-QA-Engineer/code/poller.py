import json
from typing import List, Any


def compute_moving_average(prices: List[float], window: int) -> float:
    """Compute simple moving average over the last `window` elements.
    If window <= 0 raise ValueError.
    If window > len(prices) compute average over available prices.
    Empty prices -> ValueError.
    """
    if window <= 0:
        raise ValueError("window must be > 0")
    if not prices:
        raise ValueError("prices must not be empty")
    use = prices[-window:] if window <= len(prices) else prices
    return sum(use) / len(use)


def evaluate_price_signal(price: float, ma: float, threshold_pct: float) -> str:
    """Return one of 'BUY', 'SELL', 'HOLD' based on threshold percentage.
    If price > ma*(1+threshold) -> BUY
    If price < ma*(1-threshold) -> SELL
    Otherwise HOLD
    """
    if threshold_pct < 0:
        raise ValueError("threshold_pct must be >= 0")
    upper = ma * (1 + threshold_pct)
    lower = ma * (1 - threshold_pct)
    if price > upper:
        return "BUY"
    if price < lower:
        return "SELL"
    return "HOLD"


class Poller:
    """Minimal poller abstraction used by integration tests.

    price_source must implement:
      - get_price() -> float
      - get_recent_prices(n) -> List[float]

    redis_client must implement simple get/set mapping interface for tests:
      - set(key, value)
      - get(key) -> value
    """

    def __init__(self, price_source: Any, redis_client: Any, ma_window: int = 5, threshold_pct: float = 0.01):
        self.price_source = price_source
        self.redis = redis_client
        self.ma_window = ma_window
        self.threshold_pct = threshold_pct

    def poll_once(self) -> dict:
        price = self.price_source.get_price()
        recent = self.price_source.get_recent_prices(self.ma_window)
        ma = compute_moving_average(recent, self.ma_window) if recent else price
        signal = evaluate_price_signal(price, ma, self.threshold_pct)
        payload = {"price": price, "ma": ma, "signal": signal}
        # persist last alert for downstream systems
        try:
            self.redis.set("last_alert", json.dumps(payload))
        except Exception:
            # swallow in tests; real system should log
            pass
        return payload
