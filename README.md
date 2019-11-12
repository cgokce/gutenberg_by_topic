This is a script for creating dataset with any chosen topic from the [Project Gutenberg](https://www.gutenberg.org/) Books. This is an modified version of the  [Gutenberg Poetry](https://github.com/aparrish/gutenberg-poetry-corpus) project, and contains similar code.

## Installation

Install the [Gutenberg Dammit](https://github.com/aparrish/gutenberg-dammit/) using pip:

```pip install https://github.com/aparrish/gutenberg-dammit/archive/master.zip ```

Download the corpus from the [GD](https://github.com/aparrish/gutenberg-dammit/) repository. Then clone this repository, and place the corpus in the project folder.

```git clone https://github.com/cgokce/gutenberg_by_topic.git ```

## Usage

Run the ```build.py``` with desired topic as an argument. Dataset will be created as ```dataset.txt```.

```python build.py --topic adventure```
