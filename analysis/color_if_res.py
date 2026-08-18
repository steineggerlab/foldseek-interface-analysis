# Standardized visualization of interface residues for interface clustering manuscript
# Example commands in ChimeraX to run the visualization script:
# > open color_if_res.py
# > color_if_res model #1 chain1 A chain2 B color_mode dark

from chimerax.core.commands import CmdDesc, register, StringArg, FloatArg
from chimerax.atomic import AtomicStructuresArg


def color_if_res(session, model=None, chain1=None, chain2=None, color_mode="dark"):
    """
    Standardized visualization of two interacting protein chains.

    Parameters
    ----------
    structures : list of AtomicStructure
        The structure(s) to operate on. Defaults to all open structures.
    chain1 : str
        Chain ID of the first chain.
    chain2 : str
        Chain ID of the second chain.
    cutoff : float
        Distance cutoff (Angstroms) between alpha-carbons. Default 10.0.
    """
    from chimerax.core.commands import run

    # Validate chain inputs
    if model is None or chain1 is None or chain2 is None:
        session.logger.error(
            "You must specify a model and both chain IDs, e.g. "
            "'interfaceViz chain1 A chain2 B'"
        )
        return

    # Color values
    dark_color1 = "#007A00"  # green for chain1 interface residues
    dark_color2 = "#1B0C6E"  # dark blue/indigo for chain2 interface residues
    light_color1 = "#99FF99"
    light_color2 = "#AFA3F5"
    alt_light_color1 = "#33FF33"
    alt_light_color2 = "#6047EB"
    alt_dark_color1 = "#00CC00"
    alt_dark_color2 = "#2D14B8"

    # Generic graphics settings
    run(session, f"hide {model} atoms")
    run(session, f"show {model} cartoons")
    run(session, "lighting flat")
    run(session, "graphics silhouettes true width 2")
    run(session, "set bgColor white")

    # Color entire dimer white
    run(session, f"color {model} white")

    # Construct chain-specific specifiers
    spec1 = f"{model}/{chain1}"
    spec2 = f"{model}/{chain2}"

    # Color interface residues on first chain
    run(session,
        f"select ({spec1}@CA & ({spec2}@CA @< 10.0)) residues true")
    # Either light or dark color scheme (green shades)
    if color_mode == "dark":
        run(session, f"color sel {dark_color1}")
    elif color_mode == "light":
        run(session, f"color sel {light_color1}")
    elif color_mode == "alt_light":
        run(session, f"color sel {alt_light_color1}")
    elif color_mode == "alt_dark":
        run(session, f"color sel {alt_dark_color1}")
    else:
        session.logger.error(
            "You must specify either the 'dark' or 'light' color scheme"
        )

    # Color residues on second chain
    run(session,
        f"select ({spec2}@CA & ({spec1}@CA @< 10.0)) residues true")
    # Either light or dark color scheme (blue shades)
    if color_mode == "dark":
        run(session, f"color sel {dark_color2}")
    elif color_mode == "light":
        run(session, f"color sel {light_color2}")
    elif color_mode == "alt_light":
        run(session, f"color sel {alt_light_color2}")
    elif color_mode == "alt_dark":
        run(session, f"color sel {alt_dark_color2}")
    else:
        session.logger.error(
            "You must specify either the 'dark' or 'light' color scheme"
        )

    # Clear the selection so it doesn't obscure the coloring
    run(session, "select clear")


# Register the command with ChimeraX
color_if_res_desc = CmdDesc(
    keyword=[
        ("model", StringArg),
        ("chain1", StringArg),
        ("chain2", StringArg),
        ("color_mode", StringArg)
    ],
    required_arguments=["model","chain1", "chain2"],
    synopsis="Standardized visualization of two interacting protein chains",
)

register("color_if_res", color_if_res_desc, color_if_res)