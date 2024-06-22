from obp.dataset import OpenBanditDataset


def main():
    dataset = OpenBanditDataset(behavior_policy="random", campaign="all")
    # bandit_feedback = dataset.obtain_batch_bandit_feedback()
    print(dataset)
    # print(bandit_feedback)


if __name__ == "__main__":
    main()
