import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path


def plot_broken_axis(
    labels: list[str],
    values: tuple[float, ...],
    ylim_low=(0, 12),
    ylim_high=(20, 25),
    **kwargs,
):
    """
    Строит график с разрывом оси.
    Валидирует входные данные и инкапсулирует логику отрисовки.
    """
    if len(labels) != len(values):
        raise ValueError("Длины labels и values не совпадают")

    fig, (ax_high, ax_low) = plt.subplots(
        nrows=2, figsize=(7, 4), gridspec_kw={"height_ratios": [1, 2]}
    )

    # Настройки столбцов
    kwargs.setdefault("color", "skyblue")
    kwargs.setdefault("edgecolor", "black")
    kwargs.setdefault("alpha", 0.85)

    ax_low.bar(labels, values, **kwargs)
    ax_high.bar(labels, values, **kwargs)
    fig.subplots_adjust(hspace=0.0)

    # Настройка осей
    ax_low.set_ylim(*ylim_low)
    ax_high.set_ylim(*ylim_high)
    ax_high.set_title("График с разрывом")
    ax_low.set_ylabel("Рейтинг в %")
    ax_low.set_xlabel("Языки")
    ax_high.spines["bottom"].set_visible(False)
    ax_low.spines["top"].set_visible(False)
    ax_high.tick_params(axis="x", bottom=False, labelbottom=False)
    # Рисуем разрыв оси (волна)
    offset, n_points = 0.03, 33
    pts = np.linspace(-offset, 1 + offset, n_points)
    wave = np.array([1 + (0, offset, 0, -offset)[i % 4] for i in range(n_points)])
    path = Path(list(zip(pts, wave)), [Path.MOVETO] + [Path.CURVE3] * (n_points - 1))

    opts = dict(transform=ax_low.transAxes, clip_on=False, zorder=10)
    ax_low.add_patch(mpatches.PathPatch(path, lw=6, **opts))
    ax_low.add_patch(mpatches.PathPatch(path, lw=3, edgecolor="white", **opts))
    return fig


if __name__ == "__main__":
    langs = ["Python", "C", "C++", "Asm"]
    pops = (21.8, 11.1, 8.6, 1.1)

    # Стиль xkcd
    with plt.xkcd(scale=1, length=300, randomness=30):
        plt.rcParams["font.family"] = "Comic Sans MS"

        # Вызов функции
        fig = plot_broken_axis(langs, pops)
        plt.show()
