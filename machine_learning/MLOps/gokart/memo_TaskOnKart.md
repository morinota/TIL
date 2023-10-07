## 0.1. link

- https://gokart.readthedocs.io/en/latest/task_on_kart.html

# 1. TaskOnKartクラス

- `TaskOnKart`クラスは`luigi.Task`を継承していており、タスクの定義を簡単にできる関数を持つ。
  - `luigi.Task`の詳細: https://luigi.readthedocs.io/en/stable/index.html

## 1.1. outline

## 1.2. TaskOnKart.make_target() method

## 1.3. TaskOnKart.load() method

## 1.4. TaskOnKart.dump() method

# 2. 高度な(Advancedな) 機能

## 2.1. TaskOnKart.load_generator() method

## 2.2. TaskOnKart.make_model_target() method

## 2.3. TaskOnKart.load_data_frame() method

refer to https://gokart.readthedocs.io/en/latest/for_pandas.html

## 2.4. TaskOnKart.fail_on_empty_dump() method

refer to https://gokart.readthedocs.io/en/latest/for_pandas.html

## 2.5. TaskOnKart.should_dump_supplementary_log_files() method

## 2.6. Dump(=データを一時的にメモリやtempファイル等に保存する事?) csv with encoding
