import re
 
from sys import version_info, argv
from itertools import islice   

agg_funcs = {
    'sum': sum,
    'mean': lambda x: sum(x)/len(x),
    'media': lambda x: sum(x)/len(x),
    'count': len
}


file = open("random.csv", "r")

header = file.readline()

agg_funcs_exp = r'(?:' + r'|'.join(agg_funcs.keys()) + r')'
mode_exp = fr'(?:::({agg_funcs_exp}))'
list_exp = fr'(?:{{(\d+)(?:,(\d+))?}}{mode_exp}?)'
col_exp = fr'(?:(?:(".*?"|[^,"{{}}]+){list_exp}?)?(?:,|\n))'
header_exp_check = fr'{col_exp}+'


columns = {} 
list_count = 0

for col, min_v, max_v, mode in re.findall(col_exp, header):

        col = col.strip('"')
        

        if min_v:
            opt = (int(min_v), int(max_v or min_v), (mode, agg_funcs[mode]) if mode else None)
            list_count = opt[1]
            columns[col] = opt
        else:
            columns[col] = None
            

n_columns = sum(v[1] if v else 1 for v in columns.values())



json_output = []

item_row_exp = r'(?:(".*?"|[^,]*)(?:,|$))'
row_exp_check = fr'^{item_row_exp}{{{n_columns}}}'

item_row_re = re.compile(item_row_exp)
row_re_check = re.compile(row_exp_check)




for idx, _line in enumerate(file):
    line = _line.rstrip('\n')

    if not line: 
        continue
    results = (item.strip('"') for item in item_row_re.findall(line))
    
    def get_pair(col, opt):    
        if opt:
            
            min_v, max_v, mode = opt
            r = [int(x) for x in islice(results, max_v) if x]
            if mode:
                mode_name, mode_func = mode
                
                return (col + '_' + mode_name, mode_func(r))
            
            return (col, r)
        else:
                return (col, next(results))
            
    
    values = dict(get_pair(col, opt) for col, opt in columns.items())
    json_output.append(values)



with open("resultado.json", 'w') as f:
    buffer = []
    
    f.write('[\n')

    for row in json_output:
        row_buffer = []

        result = "\t{\n"
        
        for key, value in row.items():
            row_buffer.append(f'\t\t"{key}": ' + (f'"{value}"' if isinstance(value, str) else str(value)))

        result += ',\n'.join(row_buffer) + "\n\t}"

        buffer.append(result)

    f.write(',\n'.join(buffer))

    f.write('\n]\n')