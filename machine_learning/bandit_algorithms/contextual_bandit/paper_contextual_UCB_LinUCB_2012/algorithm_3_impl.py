from typing import Any


class Policy:
    def select(self, prev_histories: list, contexts: Any) -> Any:
        pass


def off_policy_evaluation(
    T: int,
    target_policy: Policy,
    logged_events: list[dict],
):
    history_t_of = {0: []}  # initially empty history
    total_payoff_of = {0: 0}  # R_0 = initially zero total payoff
    for t in range(1, T + 1):
        # logged eventsを一つずつ見ていく
        for event in logged_events:
            # event := (x_1, ..., x_K, a, r_a)
            if target_policy(history_t_of[t - 1], event["contexts"]) != event["a"]:
                continue
            # もし現在のhistory h_{t-1} と contexts_{t} が与えられた上でtarget policyがlogging policyと同じ腕を選択する場合、
            # そのイベントはsupport(保持)される。 (i.e. historyと総報酬が更新される。)
            # (まさにnaiveなOPE!!)
            history_t_of[t] = history_t_of[t - 1] + [event]
            total_payoff_of[t] = total_payoff_of[t - 1] + event["r_a"]
            break

    return total_payoff_of[T] / T
