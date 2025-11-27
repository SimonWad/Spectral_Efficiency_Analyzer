import matplotlib.pyplot as plt
import pandas as pd
from method_lib.telescope_model import TelescopeModel


import matplotlib.pyplot as plt


def plot_telescope_data(
    telescope,
    show_total=False,
    figsize=(10, 6),
    title="Telescope Throughput Model",
    xlabel="Wavelength",
    ylabel="Throughput",
):
    """
    Plot all component curves stored in telescope.df.
    telescope.df: DataFrame indexed by wavelength
    telescope.metadata["components"]: list of component names
    """

    if telescope.df.empty:
        raise ValueError("TelescopeModel.df is empty — no data to plot.")

    plt.figure(figsize=figsize)

    # Plot each component column
    for col in telescope.df.columns:
        plt.plot(
            telescope.df.index,
            telescope.df[col],
            label=col.replace("_", " ")
        )

    # Compute & plot total throughput if requested
    if show_total:
        if len(telescope.df.columns) > 1:
            total = telescope.df.product(axis=1)
            plt.plot(
                telescope.df.index,
                total,
                linewidth=2.5,
                linestyle="--",
                label="total_throughput"
            )
        else:
            print("Only one component found — skipping total throughput.")

    plt.title(title)
    plt.xlabel(f"{xlabel} [{telescope.wavelength_unit}]")
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
