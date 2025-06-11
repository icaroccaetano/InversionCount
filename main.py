import random
import time
import numpy as np
import matplotlib.pyplot as plt

# Função não utilizada, mas incluída para referência
def count_inversions_brute_force(arr):
    """
    Função para contar inversões em um array usando o método de força bruta.
    """
    inversions = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions

def count_inversions(arr):
    """
    Função principal para contar inversões em um array usando Merge Sort.
    """
    temp_arr = [0] * len(arr)  # Array temporário para o merge
    return merge_sort_and_count(arr, temp_arr, 0, len(arr) - 1)

def merge_sort_and_count(arr, temp_arr, left, right):
    """
    Função auxiliar recursiva que divide o array e conta inversões.
    """
    inversions = 0
    if left < right:
        mid = (left + right) // 2
        inversions += merge_sort_and_count(arr, temp_arr, left, mid)
        inversions += merge_sort_and_count(arr, temp_arr, mid + 1, right)
        inversions += merge_and_count_split_inversions(arr, temp_arr, left, mid, right)
    return inversions

def merge_and_count_split_inversions(arr, temp_arr, left, mid, right):
    """
    Função que combina dois subarrays ordenados e conta inversões entre eles.
    """
    i = left      # Índice para o subarray esquerdo
    j = mid + 1   # Índice para o subarray direito
    k = left      # Índice para o array temporário
    split_inversions = 0

    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp_arr[k] = arr[i]
            i += 1
        else:
            temp_arr[k] = arr[j]
            j += 1
            # Se arr[j] é menor que arr[i], então arr[j] forma inversões com todos os elementos restantes no subarray esquerdo (do i até o mid).
            split_inversions += (mid - i + 1)
        k += 1

    # Copia os elementos restantes do subarray esquerdo (se houver)
    while i <= mid:
        temp_arr[k] = arr[i]
        k += 1
        i += 1

    # Copia os elementos restantes do subarray direito (se houver)
    while j <= right:
        temp_arr[k] = arr[j]
        k += 1
        j += 1

    # Copia os elementos de volta para o array original
    for idx in range(left, right + 1):
        arr[idx] = temp_arr[idx]

    return split_inversions

print (count_inversions([1, 2, 3, 4, 5, 6]))  # Vetor ordenado, deve retornar 0
print (count_inversions([6, 5, 4, 3, 2, 1]))  # Vetor decrescente, deve retornar 15 -> (n * (n - 1)) / 2


def generate_random_array(size):
    return [random.randint(1, size * 2) for _ in range(size)]

def measure_execution_time(algorithm, arr):
    start_time = time.perf_counter()
    arr_copy = list(arr)
    inversions = algorithm(arr_copy)
    end_time = time.perf_counter()
    return end_time - start_time, inversions

def plot_results(sizes, measured_times):
    # Calcula os valores de N log N
    n_log_n_values = [n * np.log2(n) if n > 0 else 0 for n in sizes]
    
    # Média dos fatores:
    scale_factor = np.mean([m_t / (n_log_n if n_log_n != 0 else 1) for m_t, n_log_n in zip(measured_times, n_log_n_values)])
    
    scaled_n_log_n_values = [val * scale_factor for val in n_log_n_values]

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, measured_times, 'o-', label='Tempo de Execução Real')
    plt.plot(sizes, scaled_n_log_n_values, 'r--', label=r'Complexidade Teórica ($N \log N$)')
    plt.xlabel('Tamanho da Entrada (N)')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.title('Comparação: Tempo de Execução Real vs. Complexidade Teórica Ideal (nlog N)')
    plt.legend()
    plt.grid(True)
    plt.xscale('log') # Pode ser útil para visualizar grandes variações de N
    plt.yscale('log') # Pode ser útil para visualizar grandes variações de tempo
    plt.show()

if __name__ == '__main__':
    sizes = [100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 300000, 400000, 500000, 600000, 1000000]
    measured_times_random = []

    print("Medindo tempos para arrays aleatórios...")
    for size in sizes:
        arr = generate_random_array(size)
        time_taken, num_inversoes = measure_execution_time(count_inversions, arr)
        measured_times_random.append(time_taken)
        print(f"  Tamanho {size}: {time_taken:.6f} segundos - {num_inversoes} inversões")

    # Plota os resultados para arrays aleatórios
    plot_results(sizes, measured_times_random)
