import os
import click

@click.group()
def main():
    pass

@main.command()
@click.option('--path', type=click.Path(exists=True), default=None)
def catgt(path):
    from .catgt import run_catgt
    run_catgt(path)

@main.command()
@click.option('--path', type=click.Path(exists=True), default=None)
def runks(path):
    from .ks import run_ks4
    run_ks4(path)

@main.command()
@click.option('--path', type=click.Path(exists=True), default=None)
@click.option('--metric', is_flag=True)
def saveks(path, metric):
    from .utils import finder
    from .ks import Kilosort
    fn = finder(path, 'params.py$')
    if fn is None:
        raise ValueError('No params.py found in the directory')
    fd = os.path.dirname(fn)
    ks = Kilosort(fd)
    ks.load_waveforms()
    ks.load_sync()
    ks.load_nidq()
    if metric:
        ks.load_metrics()
    ks.save()

@main.command()
@click.option('--path', type=click.Path(exists=True), default=None)
def bmi(path):
    from .bmi import BMI
    from .tdms import save_tdms
    from .utils import finder
    bmi = BMI(path)
    bmi.save_mua()
    if any(file.endswith('.nidq.meta') for file in os.listdir(path)):
        bmi.save_nidq()
    else:
       save_tdms(path=bmi.path)

@main.command()
@click.option('--path', type=click.Path(exists=True), default=None)
def tdms(path):
    from .tdms import save_tdms
    save_tdms(path)

@main.command()
@click.option('--path', type=click.Path(exists=True), default=None)
@click.option('--type', type=click.Choice(['unity', 'pi']), default='unity')
def task(path, type):
    from .task import Task
    task = Task(path=path, task_type=type)
    task.save()
    task.summary()
    task.plot()