import sys
import re

class AoCAnswers:
    def __init__(self):
        with open('day1_input.txt') as f:
            self.expense_report = []
            for line in f:
                self.expense_report.append(int(line))
        
        with open('day2_input.txt') as f:
            self.password_db = []
            for line in f:
                self.password_db.append(line)

        with open('day3_input.txt') as f:
            self.tree_map = f.readlines()
        

        with open('day4_input.txt') as f:
            self.airport_data = f.readlines()

        with open('day5_input.txt') as f:
            self.boarding_passes = []
            for line in f:
                self.boarding_passes.append(line.strip())

        with open('day6_input.txt') as f:
            self.answers = f.readlines()

        with open('day7_input.txt') as f:
            self.bag_rules = f.readlines()

        self.problems_answers = {
            'problem_1': self.problem_1,
            'problem_2': self.problem_2,
            'problem_3': self.problem_3,
            'problem_4': self.problem_4,
            'problem_5': self.problem_5,
            'problem_6': self.problem_6,
            'problem_7': self.problem_7,
            'problem_8':self.problem_8,
            'problem_9': self.problem_9,
            'problem_10':self.problem_10,
            'problem_11': self.problem_11,
            'problem_12': self.problem_12,
            'problem_13': self.problem_13
        }


    def get_ans(self, problem):
        print('gettting answer for {}'.format(problem))
        problem = self.problems_answers.get(problem)
        return problem()


    def problem_1(self, max=2020):
        expense_sheet = {}
        for first_num in self.expense_report:
            second_num = max-first_num
            if expense_sheet.get(second_num) is not None:
                print('{0} + {1} = {2}\n{0}*{1} = {3}'.format(first_num, second_num, first_num+second_num, first_num*second_num))
                return first_num*second_num
            else:
                expense_sheet[first_num] = second_num
        
        return None


    def problem_2(self):
        # x + y + z = 2000
        for x in self.expense_report:
            y_plus_z = 2020-x

            yz_product = self.problem_1(max=y_plus_z)
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


    def problem_3(self):
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
    def problem_4(self):
        num_valid = 0
        for entry in self.password_db:
            pos1, pos2, letter, password = self.clean_entry(entry)
            char1 = password[pos1-1]
            char2 = password[pos2-1]
            if char1 == letter or char2 == letter:
                if char1 != letter or char2 != letter:
                    num_valid += 1
        return num_valid


    def problem_5(self):
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
    def problem_6(self):
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
    def problem_7(self):
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

    def problem_8(self):
        self.problem_7()
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

    def problem_9(self):
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


    def problem_10(self):
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


    def problem_11(self):
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


    def problem_12(self):
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


    def problem_13(self):
        bags = {}
        for line in self.bag_rules:
            line = line.strip()
            container, containees = line.split('contain')
            container = container.strip()[:-1]
            containees = containees.split(',')
            cleaned_containees = []
            for c in containees:
                c = c.strip()
                if c.endswith('.'): c = c[:-1] 
                if re.match(r'[1-9]', c):
                    # strip off leading number
                    c = c[1:].strip()
                    # strip off trailing 's' if it exists
                    if c.endswith('s'): c = c[:-1]
                    cleaned_containees.append(c)
            bags[container] = cleaned_containees

        can_hold_gold_bag = set()
        for bag, bags_inside in bags.items():
            if 'shiny_gold_bags' in bags_inside:
                can_hold_gold_bag.add(bag)





if __name__=='__main__':
    problem = sys.argv[1]

    Advent = AoCAnswers()

    print(Advent.get_ans(problem))