# MCN-SapBERT

## Usage

### Convert cui to name
For training set:
```python
python cui2name.py --input_name train_norm
```
For testing set:
```python
python cui2name.py --input_name test_norm
```

### Show NAME-less cui
This operation will display the CUIs that could not be resolved using the `umls_api`.
For training set:
```python
python cui2name.py --input_name train_norm
```
For testing set
```python
python cui2name.py --input_name test_norm
```
### Train the model
```python
python main.py --do_train
```

### Test the model
```python
python main.py --do_eval
```
You'll be prompted to input the epoch you want to test.

## Input and Output
