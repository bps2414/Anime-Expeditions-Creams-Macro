"""
Test module for verifying CodeRabbit PR review integration.
"""

import unittest

def calculate_macro_stats(runs_completed: int, total_time_seconds: float) -> dict:
    """
    Calcular estatísticas de execução do macro.
    
    :param runs_completed: Número de partidas concluídas
    :param total_time_seconds: Tempo total decorrido em segundos
    :return: Dicionário com estatísticas calculadas
    """
    if total_time_seconds <= 0 or runs_completed < 0:
        return {"runs_per_hour": 0.0, "avg_run_time": 0.0}
    
    hours = total_time_seconds / 3600.0
    runs_per_hour = runs_completed / hours
    avg_run_time = total_time_seconds / max(1, runs_completed)
    
    return {
        "runs_per_hour": round(runs_per_hour, 2),
        "avg_run_time": round(avg_run_time, 2),
    }


class TestCodeRabbitDemo(unittest.TestCase):
    def test_calculate_macro_stats_valid(self):
        stats = calculate_macro_stats(10, 3600.0)
        self.assertEqual(stats["runs_per_hour"], 10.0)
        self.assertEqual(stats["avg_run_time"], 360.0)

    def test_calculate_macro_stats_zero_time(self):
        stats = calculate_macro_stats(5, 0.0)
        self.assertEqual(stats["runs_per_hour"], 0.0)
        self.assertEqual(stats["avg_run_time"], 0.0)


if __name__ == "__main__":
    unittest.main()
