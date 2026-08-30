"""Deterministic AI-style analytics for Market Mind.

This service produces explainable signals from available fundamentals and price inputs.
It intentionally does not claim predictive certainty or execute trades.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional


class AIService:
    """Explainable analytics for stock research and portfolio insights."""

    POSITIVE_WORDS = {
        "beat", "bullish", "gain", "growth", "improve", "outperform",
        "profit", "rally", "record", "strong", "surge", "upgrade",
    }
    NEGATIVE_WORDS = {
        "bearish", "crash", "cut", "decline", "downgrade", "drop",
        "fall", "loss", "miss", "risk", "warning", "weak",
    }

    @staticmethod
    def _number(data: Dict[str, Any], key: str, default: float = 0.0) -> float:
        value = data.get(key, default)
        try:
            return float(value) if value is not None else default
        except (TypeError, ValueError):
            return default

    def score_stock(self, stock: Dict[str, Any]) -> Dict[str, Any]:
        """Return an explainable 0-100 quality score and research stance."""
        score = 50.0
        reasons: List[str] = []
        cautions: List[str] = []

        pe = self._number(stock, "pe_ratio", 0)
        pb = self._number(stock, "pb_ratio", 0)
        roe = self._number(stock, "roe", 0)
        debt = self._number(stock, "debt_to_equity", 0)
        revenue_growth = self._number(stock, "revenue_growth", 0)
        profit_growth = self._number(stock, "profit_growth", 0)
        change = self._number(stock, "price_change_percent", 0)

        if 0 < pe <= 18:
            score += 10
            reasons.append("Reasonable earnings valuation")
        elif pe > 35:
            score -= 8
            cautions.append("Elevated earnings valuation")
        if 0 < pb <= 3:
            score += 5
        elif pb > 8:
            score -= 5
            cautions.append("Elevated book-value valuation")

        if roe >= 20:
            score += 15
            reasons.append("Strong return on equity")
        elif roe < 8:
            score -= 10
            cautions.append("Low return on equity")

        if debt <= 0.5:
            score += 10
            reasons.append("Conservative leverage")
        elif debt > 1.5:
            score -= 12
            cautions.append("High leverage")

        if revenue_growth >= 15:
            score += 8
            reasons.append("Healthy revenue growth")
        elif revenue_growth < 0:
            score -= 8
            cautions.append("Contracting revenue")
        if profit_growth >= 15:
            score += 8
            reasons.append("Healthy profit growth")
        elif profit_growth < 0:
            score -= 8
            cautions.append("Contracting profit")

        if change >= 5:
            score += 4
            reasons.append("Positive short-term momentum")
        elif change <= -8:
            score -= 5
            cautions.append("Weak short-term momentum")

        score = round(max(0, min(100, score)), 1)
        stance = "RESEARCH"
        if score >= 75:
            stance = "STRONG RESEARCH"
        elif score >= 60:
            stance = "POSITIVE RESEARCH"
        elif score < 40:
            stance = "CAUTION"

        return {
            "symbol": stock.get("symbol"),
            "ai_score": score,
            "stance": stance,
            "confidence": "EXPLAINABLE_RULE_BASED",
            "strengths": reasons,
            "risk_flags": cautions,
            "disclaimer": "Educational research signal only; not investment advice.",
        }

    def assess_risk(self, stock: Dict[str, Any]) -> Dict[str, Any]:
        """Return explainable risk score, 0 is lower risk and 100 higher risk."""
        risk = 25.0
        factors: List[str] = []
        debt = self._number(stock, "debt_to_equity", 0)
        roe = self._number(stock, "roe", 0)
        pe = self._number(stock, "pe_ratio", 0)
        change = abs(self._number(stock, "price_change_percent", 0))
        cap = self._number(stock, "market_cap", 0)

        if debt > 1:
            risk += 20
            factors.append("High debt-to-equity")
        if roe < 8:
            risk += 15
            factors.append("Low profitability")
        if pe > 40 or pe < 0:
            risk += 12
            factors.append("Valuation or earnings uncertainty")
        if change > 8:
            risk += 12
            factors.append("High recent price volatility")
        if 0 < cap < 5_000:
            risk += 10
            factors.append("Small-cap liquidity risk")

        risk = round(max(0, min(100, risk)), 1)
        level = "LOW" if risk < 35 else "MODERATE" if risk < 55 else "HIGH" if risk < 75 else "VERY HIGH"
        return {
            "symbol": stock.get("symbol"),
            "risk_score": risk,
            "risk_level": level,
            "risk_factors": factors or ["No material rule-based risk flags found"],
            "disclaimer": "Risk score is informational and does not measure all risks.",
        }

    def analyze_sentiment(self, headlines: Iterable[str]) -> Dict[str, Any]:
        """Use a transparent keyword baseline for supplied headlines."""
        positive = negative = neutral = 0
        for headline in headlines:
            words = set(str(headline).lower().replace(",", " ").replace(".", " ").split())
            pos = len(words & self.POSITIVE_WORDS)
            neg = len(words & self.NEGATIVE_WORDS)
            if pos > neg:
                positive += 1
            elif neg > pos:
                negative += 1
            else:
                neutral += 1
        total = positive + negative + neutral
        score = round((positive - negative) / total, 2) if total else 0.0
        label = "POSITIVE" if score > 0.15 else "NEGATIVE" if score < -0.15 else "NEUTRAL"
        return {
            "sentiment": label,
            "sentiment_score": score,
            "headline_count": total,
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "method": "transparent_keyword_baseline",
        }

    def detect_patterns(self, prices: List[float]) -> Dict[str, Any]:
        """Detect simple, explainable trend and support/resistance signals."""
        values = [float(price) for price in prices if price is not None]
        if len(values) < 20:
            return {"signal": "NEUTRAL", "patterns": [], "message": "At least 20 prices are required."}
        recent = values[-10:]
        support = round(min(values[-20:]), 2)
        resistance = round(max(values[-20:]), 2)
        current = values[-1]
        trend = "UPTREND" if current > recent[0] else "DOWNTREND" if current < recent[0] else "SIDEWAYS"
        patterns = [f"Short-term {trend.lower()}"]
        signal = "NEUTRAL"
        if current <= support * 1.02:
            patterns.append("Trading near 20-period support")
            signal = "BULLISH_WATCH"
        elif current >= resistance * 0.98:
            patterns.append("Trading near 20-period resistance")
            signal = "BEARISH_WATCH"
        elif trend == "UPTREND":
            signal = "BULLISH"
        elif trend == "DOWNTREND":
            signal = "BEARISH"
        return {
            "signal": signal,
            "trend": trend,
            "support": support,
            "resistance": resistance,
            "patterns": patterns,
            "disclaimer": "Technical signals are probabilistic and not trading instructions.",
        }

    def generate_smart_alerts(self, stock: Dict[str, Any], average_volume: Optional[float] = None) -> List[Dict[str, str]]:
        """Generate non-executing, actionable monitoring alerts."""
        alerts: List[Dict[str, str]] = []
        change = self._number(stock, "price_change_percent", 0)
        volume = self._number(stock, "volume", 0)
        rsi = self._number(stock, "rsi", 50)
        if change <= -5:
            alerts.append({"type": "PRICE_DROP", "severity": "HIGH", "message": f"Price is down {change:.2f}% today; review news and risk."})
        if change >= 5:
            alerts.append({"type": "PRICE_SURGE", "severity": "MEDIUM", "message": f"Price is up {change:.2f}% today; review catalyst and valuation."})
        if average_volume and volume >= average_volume * 2:
            alerts.append({"type": "VOLUME_SPIKE", "severity": "MEDIUM", "message": "Volume is at least twice the supplied average."})
        if rsi < 30:
            alerts.append({"type": "RSI_OVERSOLD", "severity": "LOW", "message": "RSI is below 30; monitor for confirmation rather than acting automatically."})
        elif rsi > 70:
            alerts.append({"type": "RSI_OVERBOUGHT", "severity": "LOW", "message": "RSI is above 70; monitor for reversal risk."})
        return alerts

    def optimize_portfolio(self, holdings: List[Dict[str, Any]], risk_tolerance: str = "MODERATE") -> Dict[str, Any]:
        """Produce diversification-oriented, non-executing rebalance suggestions."""
        if not holdings:
            return {"risk_tolerance": risk_tolerance, "suggestions": [], "message": "No holdings supplied."}
        total = sum(max(0.0, self._number(item, "current_value", 0)) for item in holdings)
        target = {"LOW": 10, "MODERATE": 15, "HIGH": 25}.get(risk_tolerance.upper(), 15)
        suggestions = []
        for item in holdings:
            value = max(0.0, self._number(item, "current_value", 0))
            weight = round(value / total * 100, 2) if total else 0
            if weight > target:
                suggestions.append({
                    "symbol": str(item.get("symbol", "UNKNOWN")),
                    "current_weight": weight,
                    "target_max_weight": target,
                    "insight": "Position concentration exceeds the illustrative limit; review diversification.",
                })
        return {
            "risk_tolerance": risk_tolerance.upper(),
            "portfolio_value": round(total, 2),
            "illustrative_max_single_position_pct": target,
            "suggestions": suggestions,
            "disclaimer": "Allocation suggestions are educational, not personalized investment advice.",
        }


ai_service = AIService()
