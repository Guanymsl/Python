echo "==evaluating correctness=="
for i in $(seq 1 3); do
    python main.py --input input_${i}.json --output output_${i}.json
    python evaluate.py --output output_${i}.json --golden golden_${i}.json
done
