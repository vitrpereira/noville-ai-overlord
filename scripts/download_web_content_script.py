import requests
from bs4 import BeautifulSoup
import os
import urllib

url = "https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-foundation-models-customize-rag.html"
output_dir = "./temp_llama_index_class"


def create_dir(dest_dir: str) -> None:
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)


def download_file(url_str, dest_dir) -> None:
    create_dir(dest_dir)
    response = requests.get(url_str)
    print(response)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a", href=True)

    for link in links:
        href = link["href"]

        if href.endswith(".html"):
            if not href.startswith("http"):
                href = urllib.parse.urljoin(url, href)

            print(f"Downloading '{href}'")
            file_response = requests.get(href)

            file_name = os.path.join(output_dir, os.path.basename(href))
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(file_response.text)


if __name__ == "__main__":
    download_file(url, output_dir)
    print("Donwload completed!")
