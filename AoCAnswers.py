import sys
import re
from collections import defaultdict
from time import sleep

class AoCAnswers:
    def __init__(self):
        with open('day1_input.txt') as f:
            self.expense_report = [int(line) for line in f]
        
        with open('day2_input.txt') as f:
            self.password_db = [line for line in f]

        with open('day3_input.txt') as f:
            self.tree_map = f.readlines()  

        with open('day4_input.txt') as f:
            self.airport_data = f.readlines()

        with open('day5_input.txt') as f:
            self.boarding_passes = [line.strip() for line in f]

        with open('day6_input.txt') as f:
            self.answers = f.readlines()

        with open('day7_input.txt') as f:
            self.bag_rules = f.readlines()

        with open('day8_input.txt') as f:
            self.boot_code = [line.strip() for line in f]

        with open('day9_input.txt') as f:
            self.xmas_data = [int(line.strip()) for line in f]

        with open('day10_input.txt') as f:
            self.joltages = [int(line.strip()) for line in f]

        with open('test_input.txt') as f:
            self.test_data = [int(line.strip()) for line in f]

        with open('day11_input.txt') as f:
            self.seats = [line.strip() for line in f]



        self.problems_answers = {
            'day1_1': self.day1_1,
            'day1_2': self.day1_2,
            'day2_1': self.day2_1,
            'day2_2': self.day2_2,
            'day3_1': self.day3_1,
            'day3_2': self.day3_2,
            'day4_1': self.day4_1,
            'day4_2': self.day4_2,
            'day5_1': self.day5_1,
            'day5_2': self.day5_2,
            'day6_1': self.day6_1,
            'day6_2': self.day6_2,
            'day7_1': self.day7_1,
            'day7_2': self.day7_2,
            'day8_1': self.day8_1,
            'day8_2': self.day8_2,
            'day9_1': self.day9_1,
            'day9_2': self.day9_2,
            'day10_1': self.day10_1,
            'day10_2': self.day10_2,
            'day11_1': self.day11_1,
            'day11_2': self.day11_2,
        }


    def get_ans(self, problem):
        print('gettting answer for {}'.format(problem))
        problem = self.problems_answers.get(problem)
        return problem()


    def day1_1(self, max=2020):
        expense_sheet = {}
        for first_num in self.expense_report:
            second_num = max-first_num
            if expense_sheet.get(second_num) is not None:
                print('{0} + {1} = {2}\n{0}*{1} = {3}'.format(first_num, second_num, first_num+second_num, first_num*second_num))
                return first_num*second_num
            else:
                expense_sheet[first_num] = second_num
        
        return None


    def day1_2(self):
        # x + y + z = 2000
        for x in self.expense_report:
            y_plus_z = 2020-x
            yz_product = self.day1_1(max=y_plus_z)
            if yz_product is not None:
                print('x={0}, yz_product={1}\n{0} * {1} = {2}'.format(x,yz_product,x*yz_product))
                return x*yz_product


    def clean_entry(self, entry):
        min_max, letter, password = entry.split(' ')
        if not isinstance(password, str): 
            print('errror on entry: '+ entry)
            print(min_max)
            print(letter)
            print(password)
            exit()    

        minimum, maximum = min_max.split('-')
        maximum = int(maximum)
        minimum = int(minimum)
        letter = letter.strip(':')
        return minimum, maximum, letter, password

    def day2_1(self):
        num_valid = 0
        for password_entry in self.password_db:
            minimum, maximum, letter, password = self.clean_entry(password_entry)
            letter_occurrences = password.count(letter)
            if minimum <= letter_occurrences and letter_occurrences <= maximum:
                num_valid += 1
        return num_valid        

    '''
    Given the same example list from above:

        1-3 a: abcde is valid: position 1 contains a and position 3 does not.
        1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
        2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.

    How many passwords are valid according to the new interpretation of the policies?
    '''
    def day2_2(self):
        num_valid = 0
        for entry in self.password_db:
            pos1, pos2, letter, password = self.clean_entry(entry)
            char1 = password[pos1-1]
            char2 = password[pos2-1]
            if char1 == letter or char2 == letter:
                if char1 != letter or char2 != letter:
                    num_valid += 1
        return num_valid


    def day3_1(self):
        pos = 0
        num_trees = 0
        max_pos = len(self.tree_map[0].strip())
        print(max_pos)
        i = 0
        for row in self.tree_map:
            pos = pos % max_pos
            if row[pos] == '#':
                num_trees += 1
            pos += 3
            i += 1
        print(num_trees, i)    
        return num_trees
    
    '''
    Determine the number of trees you would encounter if, for each of the following slopes,
    you start at the top-left corner and traverse the map all the way to the bottom:
        Right 1, down 1.
        Right 3, down 1. (This is the slope you already checked.)
        Right 5, down 1.
        Right 7, down 1.
        Right 1, down 2.
    In the above example, these slopes would find 2, 7, 3, 4, and 2 tree(s) respectively;
    multiplied together, these produce the answer 336.
    '''
    def day3_2(self):
        pos1 = pos2 = pos3 = pos4 = pos5 = 0
        num_trees1 = num_trees2 = num_trees3 = num_trees4 = num_trees5 = 0
        
        row_len = len(self.tree_map[0].strip())
        for i, row in enumerate(self.tree_map):
            pos1 %= row_len
            pos2 %= row_len
            pos3 %= row_len
            pos4 %= row_len
            pos5 %= row_len
            if row[pos1] == '#':
                num_trees1 += 1
            if row[pos2] == '#':
                num_trees2 += 1
            if row[pos3] == '#':
                num_trees3 += 1
            if row[pos4] == '#':
                num_trees4 += 1
            if i % 2 == 0:
                if row[pos5] == '#':
                    num_trees5 += 1
                pos5 += 1
        
            
            pos1 += 1
            pos2 += 3
            pos3 += 5
            pos4 += 7
        return num_trees1*num_trees2*num_trees3*num_trees4*num_trees5


    # byr (Birth Year), iyr (Issue Year), eyr (Expiration Year)
    # hgt (Height), hcl (Hair Color), ecl (Eye Color)
    # pid (Passport ID), cid (Country ID)
    def day4_1(self):
        self.passport_data = []
        num_valid = 0
        entry = {}
        for line in self.airport_data:
            line = line.strip()
            if line:
                line = line.split()
                for item in line:
                    k, v = item.split(':')
                    entry[k]= v
            else:
                keys = entry.keys()
                if all([k in keys for k in ['byr', 'iyr', 'eyr', 'hgt', 
                                            'hcl', 'ecl', 'pid']]):
                    num_valid += 1
                    self.passport_data.append(entry)
                entry = {}
        return num_valid

    '''
    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.
    '''
    def validate_year(self, year, minimum, maximum):
        try:
            year = int(year)
        except:
            return False
        return year >= minimum and year <= maximum

    def validate_height(self, num, unit, minimum, maximum):
        try:
            height = int(num.strip(unit))
        except:
            return False
        return height >= minimum and height <= maximum

    def passport_data_validation(self, key, value):
        if key == 'byr':
            return self.validate_year(value, 1920, 2002)
        elif key == 'iyr':
            return self.validate_year(value, 2010, 2020)
        elif key == 'eyr':
            return self.validate_year(value, 2020, 2030)
        elif key == 'hgt':
            if value.endswith('cm'):
                return self.validate_height(value, 'cm', 150, 193)
            elif value.endswith('in'):
                return self.validate_height(value, 'in', 59, 76)            
            else:
                return False
        elif key == 'hcl':
            if value.startswith('#'):
                value = value[1:]
                if len(value) == 6:
                    if re.search(r'[^0-9a-z]', value):
                        return False
                    return True
            return False

        elif key == 'ecl':
            options = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
            return value in options
        elif key == 'pid':
            if len(value) != 9 or re.search('[^0-9]',value):
                return False
            return True
        elif key == 'cid':
            return True
        else:
            print(key)
            print('something went wrong')

    def day4_2(self):
        self.day4_1()
        num_valid = 0
        num_w_7_keys = 0
        total = len(self.passport_data)
        for passport in self.passport_data:
            all_true = True
            if len(passport) in (7,8):
                num_w_7_keys += 1
                for k,v in passport.items():
                    if not self.passport_data_validation(k,v):
                        all_true = False
                        print(k,v)
                        break
                
                if all_true:
                    num_valid += 1    
                    
        print(num_w_7_keys, total)
        return num_valid


    def find_row_or_col(self, options, code, lower, upper):
        if len(options) == 1:
            return options[0]
        half = len(options)//2
        if code[0] == lower:
            return self.find_row_or_col(options[0:half], code[1:], lower, upper)
        elif code[0] == upper:
            return self.find_row_or_col(options[half:], code[1:], lower, upper)

    def day5_1(self):
        highest_row = 0
        highest_boarding_passes = []
        for boarding_pass in self.boarding_passes:
            row = self.find_row_or_col([i for i in range(128)], boarding_pass, 'F', 'B')
            if row > highest_row:
                highest_row = row
                highest_boarding_passes = [boarding_pass]
            if row == highest_row:
                highest_boarding_passes.append(boarding_pass)
        
        highest_seatID = 0
        for candidate in highest_boarding_passes:
            seat_code = candidate[-3:]
            seat = self.find_row_or_col([i for i in range(8)], seat_code, 'L', 'R')
            seatID = highest_row*8+seat
            if seatID > highest_seatID:
                highest_seatID = seatID
        
        return highest_seatID


    def day5_2(self):
        seat_IDs = []
        for bpass in self.boarding_passes:
            row = self.find_row_or_col([i for i in range(128)], bpass, 'F', 'B')
            col = self.find_row_or_col([i for i in range(8)], bpass[-3:], 'L', 'R')
            seat_IDs.append( (row*8) + col)
        
        seat_IDs.sort()
        print(seat_IDs)
        previous_seatID = seat_IDs[0]
        for seatID in seat_IDs[1:]:
            if seatID != previous_seatID+1:
                print(previous_seatID, seatID)
                return previous_seatID+1
            else:
                previous_seatID = seatID


    def day6_1(self):
        total_yes = 0
        answers_in_group = set()
        for line in self.answers:
            line = line.strip()
            if line:
                answers_in_group |= set(line)
            else:
                total_yes += len(answers_in_group)
                answers_in_group.clear()
        return total_yes


    def day6_2(self):
        total_all_yes = 0
        all_yes_in_group = set()
        new_group = True
        for line in self.answers:
            line = line.strip()
            if line:
                if new_group:
                    all_yes_in_group = set(line)
                    new_group = False
                else:
                    all_yes_in_group = all_yes_in_group.intersection(set(line))
            else:
                total_all_yes += len(all_yes_in_group)
                all_yes_in_group.clear()
                new_group = True
        return total_all_yes


    def day7_1(self):
        bags = defaultdict(set)
        for line in self.bag_rules:
            line = line.strip()
            outer_bag, inner_bags = line.split('contain')
            outer_bag = outer_bag.strip()[:-1]
            inner_bags = inner_bags.split(',')
            for b in inner_bags:
                b = b.strip()
                if b.endswith('.'): b = b[:-1] 
                if re.match(r'[1-9]', b):
                    # strip off leading number
                    b = b[1:].strip()
                    # strip off trailing 's' if it exists
                    if b.endswith('s'): b = b[:-1]
                
                bags[b].add(outer_bag)

        target_bags = bags['shiny gold bag']
        visited_bags = set()
        while target_bags:
            bag = target_bags.pop()
            visited_bags.add(bag)
            for outer_bag in bags.get(bag, []):
                target_bags.add(outer_bag)
        return len(visited_bags)


    def day7_2(self):
        # implement DFS algorithm
        def find_inner_bags(current_bag):
            if current_bag == 'no other bag':
                return 0
            try:
                num_cur_bag = int(current_bag[0])
            except:
                print(current_bag, current_bag[0])
                exit()
            current_bag = current_bag[1:].strip()
            total_in_bag = num_cur_bag
            for bag in bags[current_bag]:
                total_in_bag += num_cur_bag*find_inner_bags(bag)
            return total_in_bag
    
        bags = defaultdict(list)
        for line in self.bag_rules:
            line = line.strip()
            outer_bag, inner_bags = line.split(' contain ')
            outer_bag = outer_bag.rstrip('s ')
            inner_bags = inner_bags.split(',')
            for b in inner_bags:
                b = b.strip().rstrip('s. ')
                bags[outer_bag].append(b)

        print('bags in shiny gold bag = {}'.format(len(bags['shiny gold bag'])))
        return find_inner_bags(bags['shiny gold bag'][0])


    def day8_1(self, boot_code=[]):
        if not boot_code: boot_code=self.boot_code[:]
        print("testing...")
        i = 0
        acc = 0
        while i < len(boot_code):
            inst = boot_code[i]
            if 'STOP' in inst:
                return False, acc
            boot_code[i] = inst+'STOP'
            if inst.startswith('jmp'):
                # '-12' will get converted to -12 by int()
                i += int(inst[3:].strip())
            elif inst.startswith('acc'):
                acc += int(inst[3:].strip())
                i += 1
            elif inst.startswith('nop'):
                i += 1
        return True, acc


    def switch_op(self, opcode, old_op, new_op):
        return opcode.replace(old_op,new_op)
        
    def day8_2(self):
        for i, operation in enumerate(self.boot_code):
            boot_code = self.boot_code[:]
            print(i)
            if not operation.startswith('acc'):
                if operation.startswith('jmp'):
                    old_op, new_op = 'jmp','nop'
                elif operation.startswith('nop'):
                    old_op, new_op = 'nop','jmp'
                test_op = self.switch_op(operation, old_op, new_op)
                boot_code[i] = test_op
                successful, acc = self.day8_1(boot_code)
                if successful:
                    return acc
                else:
                    boot_code[i] = operation

        return 'FAILURE'


    def find_match(self, target, first_num, options25):
        second_num = target-first_num
        options25.remove(first_num)
        options24 = set(options25)
        return second_num in options24
    
    def day9_1(self, preamble = 25):
        for i in range(preamble,len(self.xmas_data)):
            options25 = sorted(self.xmas_data[i-preamble:i])          
            target = self.xmas_data[i]
            found_match = False
            for option in options25:
                options = options25[:]
                if self.find_match(target, option, options):
                    found_match = True
                    break
            if not found_match:
                return target
    
        return "All numbers can be created by adding 2 of the previous 25 numbers"

    def day9_2(self):
        target = self.day9_1(preamble = 25)
        print("target is {}".format(target))
        contiguous_list = []
        contiguous_amount = 0
        for num in self.xmas_data:
            if contiguous_amount == target:
                contiguous_list.sort()
                return contiguous_list[0] + contiguous_list[-1]
            if num != target:
                contiguous_list.append(num)
                contiguous_amount += num
                while contiguous_amount > target:
                    contiguous_amount -= contiguous_list[0]
                    contiguous_list = contiguous_list[1:]
        return("ERROR")


    def day10_1(self):
        self.joltages.sort()
        print('there are {} adaptors'.format(len(self.joltages)))
        num1s = 0
        num2s = 0
        # difference b/w highest adaptor and device
        # is always 3
        num3s = 1
        cur_jolt = 0
        for next_jolt in self.joltages:
            diff = next_jolt - cur_jolt
            if diff == 1: num1s += 1
            elif diff == 2: num2s += 1
            elif diff == 3: num3s += 1
            else: print('ERROR: diff = {}'.format(diff))
            cur_jolt = next_jolt
        print('{} * {} = '.format(num1s, num3s))
        return num1s * num3s


    def valid_adaptor(self, cur_adaptor, next_adaptor):
        return (next_adaptor - cur_adaptor) <= 3

    def adaptors_dfs(self, adaptor, options, memoized):
        
        if adaptor in memoized:
            return memoized[adaptor]
        elif not options[adaptor]:
            return 1
        else:
            memoized[adaptor] = sum([self.adaptors_dfs(a, options, memoized) for a in options[adaptor]])
            return memoized[adaptor]

        
    def day10_2(self):
        adaptors = [0]+sorted(self.joltages)
        adaptors.append(adaptors[-1]+3)
        print(adaptors)
        print(len(adaptors))
        sleep(1)
        options = {}
        for a1 in adaptors:
            options[a1]=[a for a in range(a1+1, a1+4) if a in adaptors]
        result = self.adaptors_dfs(0, options, {})
        return result

    
    def day11_1(self):
        old_seat_layout = self.seats
        new_seat_layout = ['#' if s == 'L' else s for l in self.seats for s in l]
        num_rows = len(self.seats)
        row_len = len(self.seats[0]) 
        while old_seat_layout != new_seat_layout:
            for x in range(num_rows):
                for y in range(row_len):
                    cur_seat = old_seat_layout[x][y]
                    if cur_seat == '.':
                        continue
                    seats_taken = 0
                    if x == 0: # top row
                        if y == 0: # top left corner
                            if old_seat_layout[x][y+1] == '#': seats_taken += 1
                            if old_seat_layout[x+1][y] == '#': seats_taken += 1
                            if old_seat_layout[x+1][y+1] == '#': seats_taken += 1
                        elif y == row_len-1: # top right corner
                            seats_to_check.append(old_seat_layout[x][y-1])
                            seats_to_check.append(old_seat_layout[x+1][y])
                            seats_to_check.append(old_seat_layout[x-1][y-1])
                        else: # top row other than corners
                            seats_to_check.append(old_seat_layout[x][y-1])
                            seats_to_check.append(old_seat_layout[x][y+1])
                            seats_to_check.append(old_seat_layout[x+1][y])
                            seats_to_check.append(old_seat_layout[x+1][y-1])
                            seats_to_check.append(old_seat_layout[x+1][y+1])
                    elif x == len(old_seat_layout-1): # bottom row
                        if y == 0: # bottom left corner
                            seats_to_check.append(old_seat_layout[x][y+1])
                            seats_to_check.append(old_seat_layout[x-1][y])
                            seats_to_check.append(old_seat_layout[x-1][y+1])
                        elif y == row_len-1: # bottom right corner
                            seats_to_check.append(old_seat_layout[x][y-1])
                            seats_to_check.append(old_seat_layout[x-1][y])
                            seats_to_check.append(old_seat_layout[x-1][y-1])
                        else: # top row other than corners
                            seats_to_check.append(old_seat_layout[x][y-1])
                            seats_to_check.append(old_seat_layout[x][y+1])
                            seats_to_check.append(old_seat_layout[x-1][y])
                            seats_to_check.append(old_seat_layout[x-1][y-1])
                            seats_to_check.append(old_seat_layout[x-1][y+1])
                    else: # middle rows
                        if y == 0: # left edge of row
                            seats_to_check.append(old_seat_layout[x][y+1])
                            seats_to_check.append(old_seat_layout[x-1][y])
                            seats_to_check.append(old_seat_layout[x-1][y+1])
                            seats_to_check.append(old_seat_layout[x+1][y])
                            seats_to_check.append(old_seat_layout[x+1][y+1])
                            
                        elif y == len(row)-1: # right edge of row
                            seats_to_check.append(old_seat_layout[x][y-1])
                            seats_to_check.append(old_seat_layout[x-1][y])
                            seats_to_check.append(old_seat_layout[x-1][y-1])
                            seats_to_check.append(old_seat_layout[x+1][y])
                            seats_to_check.append(old_seat_layout[x+1][y-1])
                        else: # middle seat needs 8 seats to check
                            seats_to_check.append(old_seat_layout[x][y-1])
                            seats_to_check.append(old_seat_layout[x][y+1])
                            seats_to_check.append(old_seat_layout[x-1][y])
                            seats_to_check.append(old_seat_layout[x-1][y-1])
                            seats_to_check.append(old_seat_layout[x-1][y+1])
                            seats_to_check.append(old_seat_layout[x+1][y])
                            seats_to_check.append(old_seat_layout[x+1][y-1])
                            seats_to_check.append(old_seat_layout[x+1][y+1])
                    check_seats(seats_to_check)


if __name__=='__main__':
    problem = sys.argv[1]
    Advent = AoCAnswers()
    print(Advent.get_ans(problem))