RED='\033[1;31m'
GREEN='\033[1;32m'
NC='\033[0m' # No Color
echo "==evaluating correctness=="
for i in $(seq 1 3); do
    python stack.py --input input_${i}.txt --output output_py_${i}.txt
    dline_py=$(diff output_py_${i}.txt golden_${i}.txt |  wc | awk -F ' ' '{print $1}')
    if [ "${dline_py}" -eq "0" ] && [ -f output_py_${i}.txt ] ; then
        echo -e "${GREEN}stack.py is correct in test case: input_${i}.txt${NC}"
    else
        echo -e "${RED}stack.py is incorrect in test case: input_${i}.txt${NC}"
    fi
done
echo "==evaluating runtime=="
for i in $(seq 1 3); do
    python stack.py --input input_${i}.txt
done
