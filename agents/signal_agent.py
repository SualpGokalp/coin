from agents.base_agent import BaseAgent


class SignalAgent(BaseAgent):
    def __init__(self):
        super().__init__("SignalAgent")

    def _score(self, analysis):
        scores = []

        rsi = analysis.get("rsi", 50)
        if rsi < 30:
            scores.append(80)
        elif rsi < 40:
            scores.append(40)
        elif rsi > 70:
            scores.append(-80)
        elif rsi > 60:
            scores.append(-40)
        else:
            scores.append(0)

        if analysis.get("macd", 0) > analysis.get("macd_signal", 0):
            scores.append(50)
        else:
            scores.append(-50)

        close = analysis.get("close", 0)
        upper = analysis.get("bb_upper", 0)
        lower = analysis.get("bb_lower", 0)
        if upper != lower:
            pos = (close - lower) / (upper - lower)
            scores.append(int((0.5 - pos) * 100))

        avg = sum(scores) / len(scores)

        if avg >= 60:
            sig = "STRONG_BUY"
        elif avg >= 30:
            sig = "BUY"
        elif avg <= -60:
            sig = "STRONG_SELL"
        elif avg <= -30:
            sig = "SELL"
        else:
            sig = "NEUTRAL"

        return {"signal": sig, "score": round(avg, 2)}

    def run(self, analyses):
        self.status = "running"
        signals = {}

        for symbol, analysis in analyses.items():
            result = self._score(analysis)
            signals[symbol] = result
            self.log(f"{symbol}: {result['signal']} (skor: {result['score']})")

        self.status = "done"
        self.result = signals
        return signals
