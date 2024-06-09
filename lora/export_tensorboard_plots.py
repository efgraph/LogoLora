import os
from tensorflow.python.summary.summary_iterator import summary_iterator
import matplotlib.pyplot as plt


def read_tensorboard_data(log_dir, tags):
    data = {tag: [] for tag in tags}

    for root, dirs, files in os.walk(log_dir):
        for file in files:
            if file.startswith("events.out.tfevents"):
                event_file = os.path.join(root, file)
                print(f"Processing {event_file}")
                for e in summary_iterator(event_file):
                    for v in e.summary.value:
                        if v.tag in tags:
                            data[v.tag].append((e.step, v.simple_value))

    return data


def plot_data(data, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for tag, values in data.items():
        if values:
            steps, values = zip(*values)
            plt.figure(figsize=(16, 6))
            plt.plot(steps, values, label=tag)
            plt.xlabel('Steps')
            plt.ylabel(tag)
            plt.title(f'Training {tag} over time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, f"{tag}.png"))
            plt.close()


if __name__ == "__main__":
    log_dir = "logo_lora/logs"
    output_dir = "plots_dir"
    tags = {'train_loss'}

    data = read_tensorboard_data(log_dir, tags)

    plot_data(data, output_dir)
