import matplotlib.pyplot as plt
import io


def create_pie_chart(data):
    if not data:
        return None

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(aspect="equal"))

    colors = ['#ba55d3', '#8a2be2', '#4682b4', '#20b2aa', '#ff69b4', '#9370db', '#6a5acd']

    max_index = amounts.index(max(amounts))
    explode = [0.0] * len(amounts)
    explode[max_index] = 0.1

    legend_labels = [f"{cat} ({amt} руб.)" for cat, amt in zip(categories, amounts)]

    wedges, texts, autotexts = ax.pie(
        amounts,
        explode=explode,
        colors=colors,
        autopct='%1.1f%%',
        startangle=140,
        pctdistance=0.75,
        textprops={'color': "w", 'fontsize': 12}
    )

    ax.legend(
        wedges,
        legend_labels,
        title="Категории",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        frameon=False,
        fontsize=12
    )

    fig.patch.set_facecolor('none')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    plt.close(fig)

    return buf