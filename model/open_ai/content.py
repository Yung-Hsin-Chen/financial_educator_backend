def load_files():
    """
    load files for the deterministic question answering
    Arguments:
        none
    Returns:
        None
    """
    path = "./static/explanations"
    file_lst = ["/aktien1", "/aktien2", "/aktien3", "/risiko1", "/risiko2", "/risiko3", "/risiko4", "/risiko5", \
        "/alternative_investment", "/derivatives1", "/derivatives2", "/forex1", "/forex2", "/investment_funds", \
        "/liquidity1", "/liquidity2" ,"/liquidity3", "/precious_metal"]
    docs_lst = []
    for f_name in file_lst:
        with open(path + f_name + ".txt", encoding='utf8') as f:
            docs_lst.append(f.read())

    with open(path + "/document.txt", 'w', encoding="utf8") as f:
        for text in docs_lst:
            f.write(" " + text)
