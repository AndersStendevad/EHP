from regnskab.cli import regnskab 

def test_regnskab(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(regnskab, ["world"])
        assert not result.exception
        assert result.output == 'Hello world!\n'
