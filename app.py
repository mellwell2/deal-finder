import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL
url = 'https://listado.mercadolibre.com.co/computacion/_Desde_49_Deal_promociones-colombia_Discount_5-100_NoIndex_True%22'

# Fetch the content from the URL
response = requests.get(url)
response.encoding = 'utf-8'  # Ensure the response is correctly decoded
soup = BeautifulSoup(response.text, 'html.parser')

# Extract deals
deals = []

# Define the selectors based on the page structure
items = soup.find_all('li', {'class': 'ui-search-layout__item'})

for item in items:
    title_tag = item.find('h2', {'class': 'ui-search-item__title'})
    title = title_tag.text.strip() if title_tag else 'No title'
    
    link = item.find('a', {'class': 'ui-search-link'}).get('href', '#') if item.find('a', {'class': 'ui-search-link'}) else '#'
    
    price_container = item.find('div', {'class': 'ui-search-price__second-line'})
    if price_container:
        price = price_container.find('span', {'class': 'andes-money-amount'}).get('aria-label', 'No price').strip()
    else:
        price = 'No price'
    
    discount_container = item.find('span', {'class': 'ui-search-price__discount'})
    discount = discount_container.text.strip() if discount_container else '0%'
    
    deals.append({
        'title': f'<a href="{link}" target="_blank">{title}</a>',
        'price': price,
        'discount': discount
    })

# Create a DataFrame
df = pd.DataFrame(deals)

# Generate an HTML table from the DataFrame
html_table = df.to_html(index=False, escape=False, classes='table table-striped table-hover rounded-border')

# Create an HTML file and write the table into it
html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Deals from Mercado Libre</title>
    <meta charset="UTF-8">
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .container {{
            margin-top: 20px;
        }}
        .form-control {{
            margin-bottom: 20px;
        }}
        .rounded-border {{
            border: 2px solid #ddd !important;
            border-radius: 10px !important;
        }}
        .rounded-border th,
        .rounded-border td {{
            border: 1px solid #ddd !important;
            border-radius: 5px !important;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Deals from Mercado Libre</h1>
        <div class="form-group">
            <input id="search" type="text" class="form-control" placeholder="Search" onkeyup="searchTable()">
        </div>
        <div class="table-responsive">
            {html_table}
        </div>
        <ul class="pagination justify-content-center">
            <li class="page-item disabled"><a class="page-link" href="#">Previous</a></li>
            <li class="page-item active"><a class="page-link" href="#">1</a></li>
            <li class="page-item"><a class="page-link" href="#">2</a></li>
            <li class="page-item"><a class="page-link" href="#">3</a></li>
            <li class="page-item"><a class="page-link" href="#">Next</a></li>
        </ul>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script>
        function searchTable() {{
            var input, filter, table, tr, td, i, j, txtValue;
            input = document.getElementById("search");
            filter = input.value.toUpperCase();
            table = document.querySelector("table");
            tr = table.getElementsByTagName("tr");
            for (i = 1; i < tr.length; i++) {{
                tr[i].style.display = "none";
                td = tr[i].getElementsByTagName("td");
                for (j = 0; j < td.length; j++) {{
                    if (td[j]) {{
                        txtValue = td[j].textContent || td[j].innerText;
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {{
                            tr[i].style.display = "";
                            break;
                        }}
                    }}
                }}
            }}
        }}
    </script>
</body>
</html>
'''

with open('deals.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("HTML file 'deals.html' has been created.")
