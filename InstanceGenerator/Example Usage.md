### Generate **discrete** weights
```bash
python InstanceGenerator.py 
        --output_dir instances 
        --num_instances 1 
        --min_weights [0] 
        --max_weights [10] 
        --gene_lengths [50000] 
        --discrete
```
The `--discrete` flag ensures that the generated weights are **integer values** in `[min_weight, max_weight]`.

---

### Generate **continuous** weights
```bash
python InstanceGenerator.py 
        --output_dir instances 
        --num_instances 1 
        --min_weights [0] 
        --max_weights [10] 
        --gene_lengths [50000]
```
Omitting the `--discrete` flag defaults to **floating-point weights** in `[min_weight, max_weight]`.

---

### Generate **non zero** weights
```bash
python InstanceGenerator.py 
        --output_dir instances 
        --num_instances 1 
        --min_weights [0] 
        --max_weights [10] 
        --gene_lengths [50000] 
        --no_zero
```
The `--no_zero` flag ensures that there are no zero generated weights in `[min_weight, max_weight]`.

---

### Specify a **positive percentage**
```bash
python InstanceGenerator.py 
        --output_dir instances 
        --num_instances 1 
        --min_weights [-10] 
        --max_weights [10] 
        --gene_lengths [10] 
        --discrete 
        --no_zero 
        --pos_percentage 70
```
This ensures about 70% of weights are in `[0, max_weight]` and 30% in `[min_weight, 0)` (assuming `min_weight < 0 < max_weight`).