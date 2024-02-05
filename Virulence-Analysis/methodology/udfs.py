import os
import re
import statistics as st
import sys
import warnings
from typing import List
from typing import Tuple

import numpy as np
from kneed import KneeLocator
from matplotlib import pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType
from pyspark.sql.types import DoubleType
from pyspark.sql.types import StringType
from scipy.optimize import curve_fit

sys.setrecursionlimit(10000)

PATTERN1 = re.compile(r'[~:]')


def exp_fit_func(x: np.array, a: float, b: float, c: float) -> np.array:
    return a * np.exp(-b * x) + c


def fit_data(data: Tuple[np.array, np.array]) -> Tuple[np.array, np.array]:
    x, y = data
    popt, pcov = curve_fit(exp_fit_func, x, y)
    y_fit = exp_fit_func(x, *popt)
    return x, y_fit


def plot(
        genus: str,
        data: Tuple[np.array, np.array],
        data_fit: Tuple[np.array, np.array],
        knee_locator: KneeLocator,
        save_path: str) -> None:
    genus_path = os.path.join(save_path, genus[0])
    os.makedirs(genus_path, exist_ok=True)
    fig = plt.figure(figsize=(8, 8))
    plt.plot(data[0], data[1], color='blue', marker='.', markersize=8, label='data')
    plt.plot(data_fit[0], data_fit[1], color='red', marker='.', markersize=6, label='fit')
    plt.plot(knee_locator.x, knee_locator.y, color='green', marker='.', markersize=3, label='kneedle')
    plt.vlines(knee_locator.elbow, plt.ylim()[0], plt.ylim()[1], linestyles='--', label='knee/elbow')
    plt.suptitle(genus, fontsize=16)
    plt.xticks([])
    plt.tick_params(axis='x', which='both', bottom=False, top=False)
    plt.title(f'MINIMUM CUTOFF THRESHOLD: {round(knee_locator.elbow_y)}')
    plt.xlabel('NEIGHBOR ARCHITECTURE')
    plt.ylabel('NEIGHBOR COUNT')
    plt.legend()
    plt.savefig(os.path.join(genus_path, f'{genus}.png'))
    plt.close(fig)


@udf(returnType=DoubleType())
def median(data: List[float]) -> float:
    return float(st.median(data))


@udf(returnType=DoubleType())
def mode(data: List[float]) -> float:
    return float(st.mode(data))


@udf(returnType=DoubleType())
def mct(y: List[float], genus: str, save_path: str) -> float:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            x = list(range(len(y)))
            y = list(sorted(y, reverse=True))
            data = np.array(x, dtype=np.float64), np.array(y, dtype=np.float64)
            data_fit = fit_data(data)
            knee_locator = KneeLocator(data_fit[0], data_fit[1], curve='convex', direction='decreasing')
            elbow_x, elbow_y = float(knee_locator.elbow), float(round(knee_locator.elbow_y))
            plot(genus, data, data_fit, knee_locator, save_path)
            print(f'genus={genus}, num_x={len(x)}, num_y={len(y)}, elbow_x={elbow_x}, elbow_y={elbow_y}')
            return elbow_y
    except Exception as e:
        print(f'genus={genus}, ERROR={str(e)}')
        return 0.0


@udf(returnType=ArrayType(StringType(), False))
def sort_vector(data: List[str]) -> List[str]:
    return list(sorted(data, key=lambda r: int(re.split(PATTERN1, r)[0])))


def register(spark: SparkSession) -> None:
    spark.udf.register('median', median)
    spark.udf.register('mode', mode)
    spark.udf.register('mct', mct)
    spark.udf.register('sort_vector', sort_vector)
