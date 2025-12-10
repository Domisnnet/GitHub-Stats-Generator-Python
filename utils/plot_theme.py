import matplotlib.pyplot as plt

def apply_dark_tech_theme():
    plt.style.use("default")

    plt.rcParams.update({
        # Fundo
        "figure.facecolor": "#0d1117",
        "axes.facecolor": "#0d1117",
        "savefig.facecolor": "#0d1117",

        # Texto
        "text.color": "#e6edf3",
        "axes.labelcolor": "#e6edf3",
        "xtick.color": "#8b949e",
        "ytick.color": "#8b949e",

        # grade
        "axes.grid": True,
        "grid.color": "#30363d",
        "grid.alpha": 0.35,

        # Paleta neon
        "axes.prop_cycle": plt.cycler(color=[
            "#00eaff",  # cyan tech
            "#7b2ff7",  # roxo neon
            "#39ff14"   # verde neon
        ]),

        # Fonte
        "font.size": 11,

        # Bordas
        "axes.edgecolor": "#00eaff"
    })
