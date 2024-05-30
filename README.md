# Noville AI Overlord

This is Noville's AI base. It's a work in progress. Its goal is to host all Noville's AI agents and initiatives, handling all the logic related to connecting to models, content search and vectorization for context, and related topics.

## How to contribute

To contribute, you will need to have Python 3.11 or higher.

Install Python by running:

```shell
pip3 install python
```

### Setting Up Your Development Environment

1. First, clone the repository to your local machine.

```shell
git clone https://github.com/yourusername/noville-ai-overlord.git
```

2. Then access the project running
```shell
cd noville-ai-overlord
```

3. Create a Virtual Environment: It is recommended to use a virtual environment to manage your dependencies.

```shell
python3 -m venv your_chosen_environment
source env/bin/activate
```

If you are on Windows use 
```shell
env\Scripts\activate
```

4. Install Dependencies: 

Install the necessary dependencies from the `requirements.txt` file.
```shell
pip install -r requirements.txt
```

5. Run the Application: To ensure everything is set up correctly, run the application.

```shell
python main.py
```


### Coding Guidelines
To maintain code quality and consistency, please follow these guidelines:

- Code Style: Follow PEP 8 for Python code.
- Testing: Write unit tests for your code. Ensure that all tests pass before submitting a pull request.
- Documentation: Update the documentation for any changes or new features. Ensure your code is well-documented.
- Submitting a Pull Request
- Fork the Repository: Fork the repository to your GitHub account.

#### Recommendation: use black

Black is a code formatter for Python, guaranteeing code stardatization and organization.

- Install black

```shell
pip install black
```

- Run it

```shell
black .
```

### Contributing 
- Create a Branch: Create a new branch for your feature or bug fix.

```shell
git checkout -b feature-name
```

- Make Your Changes: Commit your changes with clear and concise commit messages.
```shell
git commit -m "Description of the changes made"
```

- Push to Your Fork: Push your changes to your forked repository.
```shell
git push origin feature-name
```

Submit a Pull Request: Go to the original repository and submit a pull request.

- Reporting Issues
If you encounter any issues or have suggestions for improvements, please create an issue on the GitHub repository. Provide as much detail as possible to help us understand and address the issue.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

Thank you for contributing to Noville AI Overlord! If you have any questions, feel free to reach out to the @vitrpereira.

Happy coding!
