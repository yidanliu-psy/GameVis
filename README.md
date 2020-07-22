# final project
_code_ &amp; _data_ &amp; _more_ for my MSc final project

## Reproducing [the paper results of Landfried et al.](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0211014)

- data: [two tables](https://drive.google.com/drive/folders/13LUQjrzp11D7h1SkU5EX7J2cN78mY6sz?usp=sharing) 
  - respectively selected columns of `play` and `game`; dumped from the original database)
- code: [here](./reproduce.py)
  - current version: please set hyper-parameter `N` (e.g., 100 or 200) which denotes the number of games considered per player
  - the code will return the digest stats of the multivariable linear regression. For example, when `N = 100`, you will get
  
  ![n=100](./figs/reproduce_n_100.jpg)
  
