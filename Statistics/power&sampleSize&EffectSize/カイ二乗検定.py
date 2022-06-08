import pandas as pd


if __name__ == "__main__":

    observed_values = [[14929, 1498], [14911, 1628]]
    p1 = 0.1
    p2 = 0.11
    sample_size = sample_power_probtest(p1, p2)
    # よってA/Bテストを仮定した場合、14752*2~29504人に無作為に施策AとBのいずれかを提示して、その結果に対し、検定を行えばよいことになる。
    print(sample_size * 2)
