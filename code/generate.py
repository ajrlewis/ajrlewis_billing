import json
import subprocess


# Helpers
def sanitize(text: str) -> str:
    chars = ["%", "&", "_"]
    for c in chars:
        text = text.replace(c, f"\\{c}")
    math_chars = [">"]
    for c in math_chars:
        text = text.replace(c, f"${c}$")
    text = text.replace("btc", "\\bitcoin{{}}")
    text = text.replace("A.J.R. Lewis", "A.J.R.\\ Lewis")
    return text


# Renders
def render_json_to_latex_agreement(json_data: dict) -> str:
    latex_code = ""

    # Render Project Details section
    latex_code += "\\section{Project Details}\n"
    project_details = json_data["Project Details"]

    for key, value in project_details.items():
        latex_code += "\\subsection{" + sanitize(key) + "}"
        latex_code += sanitize(value)
    latex_code += "\n"

    # Render Outline of Proposed Work section
    latex_code += "\\section{Outline of Proposed Work}\n"
    for key, value in json_data["Outline of Proposed Work"].items():
        latex_code += "\\subsection{" + sanitize(key) + "}"
        latex_code += "    \\begin{itemize}\n"
        values = value.split(".")
        for value in values:
            if value:
                latex_code += "        \\item " + sanitize(value.strip()) + ". \n"
        latex_code += "    \\end{itemize}\n"

    # Render Project Details section
    latex_code += "\\section{Success Criteria}\n"
    latex_code += "\\begin{enumerate}\n"
    success_criteria = json_data["Success Criteria"]
    for criteria in success_criteria:
        latex_code += "    \\item " + sanitize(criteria) + " \\\\\n"
    latex_code += "\\end{enumerate}\n"

    latex_code += "\\section{Payment Address}\n"
    latex_code += "    All payments should be made to the following address:\n"
    address = json_data["BTC Address"]
    latex_code += "    \\begin{figure*}[h!]\n"
    latex_code += "        \\centering\n"
    latex_code += (
        "        \\includegraphics[width=0.4\\textwidth]{"
        + f"data/{address}.png"
        + "}\n"
    )
    latex_code += (
        "        \\caption{"
        + "\\href{{https://mempool.space/address/"
        + address
        + "}}{{"
        + address
        + "}} }\n"
    )
    latex_code += "    \\end{figure*}\n"

    # Render Project Details section
    latex_code += "\\section{Terms \& Conditions}\n"
    success_criteria = json_data["Terms & Conditions"]
    for key, value in success_criteria.items():
        latex_code += "\\subsection{" + sanitize(key) + "}"
        latex_code += "    " + sanitize(value)

    latex_code += "\\section{Signature}"
    latex_code += "\\vspace{10em}"
    latex_code += "\\noindent"
    latex_code += "\\begin{minipage}[t]{0.4\\linewidth}"
    latex_code += "    \\dotfill \\\\"
    latex_code += "    Signature of the client"
    latex_code += "\\end{minipage}"
    latex_code += "\\hfill"
    latex_code += "\\begin{minipage}[t]{0.4\\linewidth}"
    latex_code += "    \\dotfill \\\\"
    latex_code += "    Date"
    latex_code += "\\end{minipage}"

    return latex_code


def render_json_to_latex_receipt(json_data: dict) -> str:
    latex_code = ""

    transaction_ids = json_data["Transaction IDs"]
    title = json_data["Project Details"]["Title"]
    cost = json_data["Project Details"]["Estimated Cost"]

    latex_code += "\\begin{table}[h]\n"
    latex_code += "    \\centering\n"
    latex_code += "    \\begin{tabular}{@{}lll@{}}\n"
    latex_code += "        \\toprule\n"
    latex_code += "        \\textbf{Description} & \\textbf{Amount} \\\\\n"
    latex_code += "        \\midrule\n"
    latex_code += f"        {title} & {cost.replace('btc', '')}\\\\ \n"
    latex_code += "        \\\\\n"
    latex_code += "        \\midrule\n"
    latex_code += "        \\\\\n"
    latex_code += (
        f"        \\textbf{{Total}} & \\textit{{\\textbf{{{sanitize(cost)}}}}} \\\\ \n"
    )
    latex_code += "        \\bottomrule\n"
    latex_code += "    \\end{tabular}\n"
    latex_code += "\\end{table}\n"

    # Render transaction IDs

    latex_code += "\\begin{table}[h]\n"
    latex_code += "    \\centering\n"
    latex_code += "    \\begin{tabular}{@{}ll@{}}\n"
    latex_code += "        \\toprule\n"
    latex_code += "        \\textbf{Date} & \\textbf{Transaction ID} \\\\ \\midrule"

    for date, transaction_id in transaction_ids.items():
        latex_code += f"        {date} & \\href{{https://mempool.space/tx/{transaction_id}}}{{{transaction_id}}} \\\\\n"
    # latex_code += "        2024-03-26 13:54 & \href{https://mempool.space/tx/6a88d948c5794d351b00f447974df7551016043b47d2e93eb7b17d726a38353e}{6a88d948c5794d351b00f447974df7551016043b47d2e93eb7b17d726a38353e} \\"
    latex_code += "        \\bottomrule"
    latex_code += "    \\end{tabular}"
    latex_code += "\\end{table}"

    return latex_code


def main():
    reference = "GLRH3AZC - 1"
    _type = "Agreement"
    # _type = "Receipt"

    # Render body
    body = ""
    with open(f"data/{reference}.json", "r") as f:
        json_data = json.load(f)
        client = json_data["Client"]

        if _type == "Agreement":
            body = render_json_to_latex_agreement(json_data)
        elif _type == "Receipt":
            body = render_json_to_latex_receipt(json_data)

        filename = f"AJR Lewis - {_type} - {reference}"

    # Read the base template
    template_file = "templates/base.tex"
    template = ""
    with open(template_file, "r") as f:
        template = f.read()

    # Replace keywords
    template = template.replace("% TYPE", _type)
    template = template.replace("% CLIENT", client)
    template = template.replace("% REFERENCE", f"\\#AJRLEWIS-{reference}")
    template = template.replace("% BODY", body)

    # Write template
    with open(f"{filename}.tex", "w") as f:
        f.write(template)

    # Compile twice for links
    subprocess.run(["pdflatex", f"{filename}"])
    subprocess.run(["pdflatex", f"{filename}"])

    # Tidy up
    subprocess.run(["rm", f"{filename}.aux"])
    subprocess.run(["rm", f"{filename}.out"])
    subprocess.run(["rm", f"{filename}.log"])
    subprocess.run(["mv", f"{filename}.tex", "data/"])
    subprocess.run(["mv", f"{filename}.pdf", "data/"])

    # Open
    subprocess.run(["open", f"data/{filename}.pdf"])


if __name__ == "__main__":
    main()
