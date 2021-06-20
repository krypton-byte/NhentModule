# Install

```bash
> pip instal doujin2pdf
```
# Shell
```
> python -m doujin --nuklir=123456
> python -m doujin --nuklir=123456 --output=test.pdf
```

# Python Interpreter
## Save To File
```python
>>> import doujin
>>> x=doujin.nhentai("123456").doujin
>>> x.save_to_file(x.title)
```
 ## BytesIO
 ```python
 >>> import doujin
>>> x=doujin.nhentai("123456").doujin
>>> x.download()
```