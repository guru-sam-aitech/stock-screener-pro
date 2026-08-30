"""Test script for AI Analytics API endpoints.

Usage:
    python scripts/test_ai_endpoints.py

Make sure the backend is running at http://localhost:8000
"""

import requests
import json
from typing import Any, Dict

BASE_URL = "http://localhost:8000"


def test_health() -> bool:
    """Test AI health endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/api/ai/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "ai-analytics"
        print("✅ Health check passed")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_score() -> bool:
    """Test AI scoring endpoint."""
    try:
        payload = {
            "symbol": "AAPL",
            "pe_ratio": 28.5,
            "pb_ratio": 45.2,
            "roe": 147.5,
            "debt_to_equity": 1.73,
            "revenue_growth": 8.5,
            "profit_growth": 10.2,
            "price_change_percent": 1.5,
            "market_cap": 2800000
        }
        response = requests.post(f"{BASE_URL}/api/ai/score", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "ai_score" in data
        assert "stance" in data
        assert "strengths" in data
        assert "risk_flags" in data
        assert 0 <= data["ai_score"] <= 100
        
        print(f"✅ Score test passed - Score: {data['ai_score']}, Stance: {data['stance']}")
        return True
    except Exception as e:
        print(f"❌ Score test failed: {e}")
        return False


def test_risk() -> bool:
    """Test risk assessment endpoint."""
    try:
        payload = {
            "symbol": "AAPL",
            "pe_ratio": 28.5,
            "roe": 147.5,
            "debt_to_equity": 1.73,
            "price_change_percent": 1.5,
            "market_cap": 2800000
        }
        response = requests.post(f"{BASE_URL}/api/ai/risk", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "risk_score" in data
        assert "risk_level" in data
        assert "risk_factors" in data
        assert 0 <= data["risk_score"] <= 100
        assert data["risk_level"] in ["LOW", "MODERATE", "HIGH", "VERY HIGH"]
        
        print(f"✅ Risk test passed - Risk: {data['risk_level']} ({data['risk_score']})")
        return True
    except Exception as e:
        print(f"❌ Risk test failed: {e}")
        return False


def test_sentiment() -> bool:
    """Test sentiment analysis endpoint."""
    try:
        payload = {
            "headlines": [
                "Apple beats earnings expectations with strong iPhone sales",
                "Tech sector faces headwinds amid rate concerns",
                "Apple announces record services revenue"
            ]
        }
        response = requests.post(f"{BASE_URL}/api/ai/sentiment", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "sentiment" in data
        assert "sentiment_score" in data
        assert "positive" in data
        assert "negative" in data
        assert "neutral" in data
        assert data["sentiment"] in ["POSITIVE", "NEUTRAL", "NEGATIVE"]
        
        print(f"✅ Sentiment test passed - Sentiment: {data['sentiment']} ({data['sentiment_score']})")
        return True
    except Exception as e:
        print(f"❌ Sentiment test failed: {e}")
        return False


def test_patterns() -> bool:
    """Test pattern detection endpoint."""
    try:
        # Generate sample price data (uptrend)
        prices = [100 + i * 0.5 + (i % 3) for i in range(30)]
        payload = {"prices": prices}
        response = requests.post(f"{BASE_URL}/api/ai/patterns", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "signal" in data
        assert "trend" in data
        assert "support" in data
        assert "resistance" in data
        assert "patterns" in data
        assert data["signal"] in ["BULLISH", "BEARISH", "BULLISH_WATCH", "BEARISH_WATCH", "NEUTRAL"]
        
        print(f"✅ Patterns test passed - Signal: {data['signal']}, Trend: {data['trend']}")
        return True
    except Exception as e:
        print(f"❌ Patterns test failed: {e}")
        return False


def test_alerts() -> bool:
    """Test smart alerts endpoint."""
    try:
        payload = {
            "symbol": "AAPL",
            "price_change_percent": -6.5,
            "volume": 125000000,
            "rsi": 28.5
        }
        response = requests.post(f"{BASE_URL}/api/ai/alerts", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert isinstance(data, list)
        assert len(data) > 0
        
        for alert in data:
            assert "type" in alert
            assert "severity" in alert
            assert "message" in alert
            assert alert["severity"] in ["LOW", "MEDIUM", "HIGH"]
        
        print(f"✅ Alerts test passed - Generated {len(data)} alerts")
        return True
    except Exception as e:
        print(f"❌ Alerts test failed: {e}")
        return False


def test_portfolio() -> bool:
    """Test portfolio optimization endpoint."""
    try:
        payload = {
            "holdings": [
                {"symbol": "AAPL", "current_value": 50000},
                {"symbol": "GOOGL", "current_value": 30000},
                {"symbol": "MSFT", "current_value": 20000}
            ],
            "risk_tolerance": "MODERATE"
        }
        response = requests.post(f"{BASE_URL}/api/ai/portfolio/optimize", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "risk_tolerance" in data
        assert "portfolio_value" in data
        assert "suggestions" in data
        assert data["risk_tolerance"] == "MODERATE"
        assert data["portfolio_value"] == 100000.0
        
        print(f"✅ Portfolio test passed - Value: ${data['portfolio_value']}, Suggestions: {len(data['suggestions'])}")
        return True
    except Exception as e:
        print(f"❌ Portfolio test failed: {e}")
        return False


def run_all_tests():
    """Run all AI endpoint tests."""
    print("=" * 60)
    print("AI Analytics API Test Suite")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}\n")
    
    tests = [
        ("Health Check", test_health),
        ("AI Scoring", test_score),
        ("Risk Assessment", test_risk),
        ("Sentiment Analysis", test_sentiment),
        ("Pattern Detection", test_patterns),
        ("Smart Alerts", test_alerts),
        ("Portfolio Optimization", test_portfolio),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\nTesting {name}...")
        result = test_func()
        results.append((name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
