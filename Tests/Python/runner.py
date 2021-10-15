from insanonym_utils import runner, models
model = models.FileConfigModel.parse_file('parser.cfg')

r = runner.Runner(model)


r.execute()