import pandas as pd
import matplotlib.pyplot as plt

before = pd.read_csv("before.csv")
after = pd.read_csv("after.csv")

plt.figure(figsize=(8,5))

plt.plot(
    before["usuarios"],
    before["latencia_media_s"],
    marker="o",
    label="Antes"
)

plt.plot(
    after["usuarios"],
    after["latencia_media_s"],
    marker="o",
    label="Despues"
)

plt.xlabel("Usuarios")
plt.ylabel("Latencia (s)")
plt.title("Latencia Antes vs Despues")
plt.legend()
plt.grid(True)

plt.savefig("comparativa_latencia.png")

plt.clf()

plt.plot(
    before["usuarios"],
    before["tokens_s"],
    marker="o",
    label="Antes"
)

plt.plot(
    after["usuarios"],
    after["tokens_s"],
    marker="o",
    label="Despues"
)

plt.xlabel("Usuarios")
plt.ylabel("Tokens/s")
plt.title("Tokens/s Antes vs Despues")
plt.legend()
plt.grid(True)

plt.savefig("comparativa_tokens.png")

print("Graficas creadas")