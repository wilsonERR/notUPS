# Mark Wilson
# Student ID:  010314264
import csv
import datetime


# Hash-map - copied from lecture, may need to add functions or make more original
class HashMap:
    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])


class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes, status, time_of_delivery):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.time_of_delivery = time_of_delivery

    def __str__(self):
        return '%s, %s, %s, %s, %s, %s, %s, %s, %s' % (self.package_id, self.address, self.city, self.state,
                                                       self.zip_code, self.deadline, self.weight, self.status,
                                                       self.time_of_delivery)

    def __repr__(self):
        return str(self)


class Truck:
    def __init__(self):
        self.mph = 18.0
        self.payload = []
        self.time = 8.00
        self.mileage = 0.0
        self.current_location = 0


def package_csv(filename):
    with open(filename, encoding='utf-8') as packages:
        package_data = csv.reader(packages, delimiter=',')
        next(package_data)
        for package in package_data:
            p_id = int(package[0])
            p_address = package[1]
            p_city = package[2]
            p_state = package[3]
            p_zip = package[4]
            p_deadline = package[5]
            p_weight = package[6]
            p_notes = package[7]
            p_status = 'At Hub'
            p_time_of_delivery = None

            p = Package(p_id, p_address, p_city, p_state, p_zip, p_deadline, p_weight, p_notes, p_status,
                        p_time_of_delivery)

            package_hash.insert(p_id, p)


def address_csv(filename):
    with open(filename, encoding='utf-8-sig') as addresses:
        address_data = csv.reader(addresses, delimiter=',')
        for address in address_data:
            loc_id = int(address[0])
            loc_address = address[1]

            address_lookup[loc_address] = loc_id


def update_address(p_id, address, city, state, zip_code):
    package = package_hash.search(p_id)
    package.address = address
    package.city = city
    package.state = state
    package.zip_code = zip_code


def load_truck(truck, package_ids):
    for p in range(1, 40):

        if package_hash.search(p).package_id in package_ids:
            truck.payload.append(package_hash.search(p))


def get_distance(loc_1, loc_2):
    return float(distance_table[loc_1][loc_2])


def convert_float_time_to_hm(time_float):
    converted_time = str(datetime.timedelta(hours=time_float))[:-3]
    if len(converted_time) == 4:
        return '0' + converted_time
    else:
        return converted_time


def convert_hm_time_to_float(time_hms):
    hours = float(time_hms[0:2])
    minutes = (float(time_hms[3:5]))/60
    return hours + minutes


def get_min_distance(truck, location):
    min_distance = 9000.0
    for p in range(len(truck.payload)):
        if get_distance(location, address_lookup.get(truck.payload[p].address)) <= min_distance:
            min_distance = get_distance(location, address_lookup.get(truck.payload[p].address))

    return min_distance


def get_total_mileage():
    total_mileage = truck_1.mileage + truck_2.mileage + truck_3.mileage
    return total_mileage


def deliver_packages(truck, start_time):
    truck.end_time = start_time
    time_counter = convert_hm_time_to_float(start_time)
    current_location = 0

    for p in range(len(truck.payload)):
        (package_hash.search(truck.payload[p].package_id)).status = 'In Transit'

    while len(truck.payload) != 0:

        min_distance = 9000.0
        package_index = None
        next_location = None

        for p in range(len(truck.payload)):

            if get_distance(current_location, address_lookup.get(truck.payload[p].address)) <= min_distance:
                min_distance = get_distance(current_location, address_lookup.get(truck.payload[p].address))
                next_location = address_lookup.get(truck.payload[p].address)
                package_index = p

        current_location = next_location
        (package_hash.search(truck.payload[package_index].package_id)).status = 'Delivered'
        time_counter += (min_distance/truck.mph)
        truck.end_time = convert_float_time_to_hm(time_counter)
        (package_hash.search(truck.payload[package_index].package_id)).time_of_delivery = truck.end_time
        truck.mileage += min_distance
        truck.payload.pop(package_index)

    truck.mileage += get_distance(current_location, 0)
    truck.end_time = convert_float_time_to_hm(time_counter + (get_distance(current_location, 0) / truck.mph))


def deliver_packages_until_end_time(truck, start_time, end_time):
    # check end time against start time: if end time is before truck is scheduled to leave, no code is run
    truck.time = start_time
    stop_time = convert_hm_time_to_float(end_time)
    time_counter = convert_hm_time_to_float(start_time)
    current_location = 0

    for p in range(len(truck.payload)):
        (package_hash.search(truck.payload[p].package_id)).status = 'In Transit'

    while len(truck.payload) != 0:

        min_distance = 9000.0
        package_index = None
        next_location = None

        for p in range(len(truck.payload)):

            if get_distance(current_location, address_lookup.get(truck.payload[p].address)) <= min_distance:
                min_distance = get_distance(current_location, address_lookup.get(truck.payload[p].address))
                next_location = address_lookup.get(truck.payload[p].address)
                package_index = p

        time_counter += (min_distance/truck.mph)
        if time_counter > stop_time:
            break

        current_location = next_location
        truck.time = convert_float_time_to_hm(time_counter)
        (package_hash.search(truck.payload[package_index].package_id)).time_of_delivery = truck.time
        truck.mileage += min_distance
        (package_hash.search(truck.payload[package_index].package_id)).status = 'Delivered'
        truck.payload.pop(package_index)

    if time_counter <= stop_time:
        truck.mileage += get_distance(current_location, 0)
        truck.time = convert_float_time_to_hm(time_counter + (get_distance(current_location, 0) / truck.mph))


package_hash = HashMap()

address_lookup = {}

truck_1 = Truck()
truck_2 = Truck()
truck_3 = Truck()

distance_table = list(csv.reader(open('distance.csv', encoding='utf-8-sig')))

package_csv('packages.csv')
address_csv('address.csv')


class Main:
    def __init__(self):
        pass

    update_address(9, '410 S State St', 'Salt Lake City', 'UT', '84111')

    load_truck(truck_1, {1, 2, 8, 13, 14, 15, 16, 20, 21, 27, 30, 34, 35, 39, 40})
    load_truck(truck_2, {3, 5, 6, 7, 12, 18, 25, 26, 29, 31, 32, 36, 37, 38})
    load_truck(truck_3, {4, 9, 10, 11, 17, 19, 22, 23, 24, 28, 33})

    truck_1.time = '08:00'
    truck_2.time = '09:06'
    truck_3.time = '10:30'

    deliver_packages(truck_1, '08:00')
    deliver_packages(truck_2, '09:06')
    deliver_packages(truck_3, '10:30')
    start = None

    while start != '0':
        print('Welcome to WGUPS package tracking')
        print('All deliveries were completed in ', "{0:.2f}".format(get_total_mileage(), 2), 'miles.')
        print('Please enter a number from the following menu')
        start = input(
            '1 - Package lookup \n2 - View status of all packages at a specific time \n0 - exit the program\n\n')
        if start == '1':
            p_id = input('Enter the package ID: ')

            print(package_hash.search(int(p_id)))
            exit()

        if start == '2':
            end_time = input('Enter a time in military time (HH:MM): ')
            # time mechanism still needs to be developed
            load_truck(truck_1, {1, 2, 8, 13, 14, 15, 16, 20, 21, 27, 30, 34, 35, 39, 40})
            load_truck(truck_2, {3, 5, 6, 7, 12, 18, 25, 26, 29, 31, 32, 36, 37, 38})
            load_truck(truck_3, {4, 9, 10, 11, 17, 19, 22, 23, 24, 28, 33})

            for p in range(1, 40):
                package_hash.search(p).status = 'At Hub'
                package_hash.search(p).time_of_delivery = ''

            deliver_packages_until_end_time(truck_1, '08:00', end_time)
            deliver_packages_until_end_time(truck_2, '09:06', end_time)
            deliver_packages_until_end_time(truck_3, '10:30', end_time)

            for i in range(1, 40):
                print(package_hash.search(i))

            exit()

        if start not in ['1', '2', '0']:
            print('Incorrect selection\n')

    print('Goodbye!')
    exit()


