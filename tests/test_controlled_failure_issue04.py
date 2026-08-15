def test_controlled_failure_blocks_pipeline():
    """Falha intencional e temporária para demonstrar o bloqueio do CI."""
    assert False, "falha controlada da ISSUE-04"
