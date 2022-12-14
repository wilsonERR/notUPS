# Mark Wilson
# Student ID:  010314264
import csv
import datetime


class HashTable:
    def __init__(self, capacity=10):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    # O(N) inserts a package into the hash table
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

    # O(N) Returns a value from the hash table
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    # O(N) deletes a value from the hash table
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])


class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes, truck_id, status,
                 time_of_delivery):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.truck_id = truck_id
        self.status = status
        self.time_of_delivery = time_of_delivery

    def __str__(self):

        if self.time_of_delivery == '':
            return 'Package ID: %s  Address: %s, %s %s, %s  Deadline: %s  Weight: %skg  Truck: %s  Status: %s%s' % \
                                                    (self.package_id, self.address, self.city, self.state,
                                                     self.zip_code, self.deadline, self.weight, self.truck_id,
                                                     self.status, self.time_of_delivery)
        else:
            return 'Package ID: %s  Address: %s, %s %s, %s  Deadline: %s  Weight: %skg  Truck: %s  Status: %s at %s' %\
                   (self.package_id, self.address, self.city, self.state,
                    self.zip_code, self.deadline, self.weight, self.truck_id,
                    self.status, self.time_of_delivery)

    def __repr__(self):
        return str(self)


class Truck:
    def __init__(self):
        self.id = None
        self.mph = 18.0
        self.payload = []
        self.time = 8.00
        self.mileage = 0.0
        self.current_location = 0


# O(N) Loads a number of packages from a csv file, and inserts each package into the hash table.
# param: filename: the path of a csv file
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
            p_truck_id = None
            p_status = 'At Hub'
            p_time_of_delivery = None

            p = Package(p_id, p_address, p_city, p_state, p_zip, p_deadline, p_weight, p_notes, p_truck_id,
                        p_status, p_time_of_delivery)

            package_hash.insert(p_id, p)


# O(N) Loads a number of addresses along with a corresponding location id from a csv. Each location is loaded
# into a dictionary that uses the address as a key to access its corresponding location id.
def address_csv(filename):
    with open(filename, encoding='utf-8-sig') as addresses:
        address_data = csv.reader(addresses, delimiter=',')
        for address in address_data:
            loc_id = int(address[0])
            loc_address = address[1]

            address_lookup[loc_address] = loc_id


# O(1) Updates a package's address attributes
# Parameter: p_id: the package's package id
#            address: the updated address
#            city: the updated city
#            state: the updated state
#            zip_code: the updated zip code
def update_address(p_id, address, city, state, zip_code):
    package = package_hash.search(p_id)
    package.address = address
    package.city = city
    package.state = state
    package.zip_code = zip_code


# O(N) Loads the packages into the truck's payload array
# Parameter: truck: a Truck object
#            package_ids: a set of package ids
def load_truck(truck, package_ids):
    for p in range(1, 41):

        if package_hash.search(p).package_id in package_ids:
            truck.payload.append(package_hash.search(p))


# O(1) Returns a float value corresponding to the distance between two locations
# Parameter: loc_1: the location id of the starting location
#            loc_2: the location id of the end location
def get_distance(loc_1, loc_2):
    return float(distance_table[loc_1][loc_2])


# O(1) Converts a time stored as a float to a string in 'HH:MM' format
# Parameter: time_float: a time represented as a float
def convert_float_time_to_hm(time_float):
    converted_time = str(datetime.timedelta(hours=time_float))[:-3]
    if len(converted_time) == 4:
        return '0' + converted_time
    else:
        return converted_time


# O(1) Converts a time stored as a string in 'HH:MM' format to a float
# Parameter: time_hms: a time represented as a string in 'HH:MM' format
def convert_hm_time_to_float(time_hms):
    hours = float(time_hms[0:2])
    minutes = (float(time_hms[3:5]))/60
    return hours + minutes


# O(1) Returns the total mileage of all trucks
def get_total_mileage():
    total_mileage = truck_1.mileage + truck_2.mileage + truck_3.mileage
    return total_mileage


# O(N^2) The following is a 'Greedy Algorithm' approach to delivering the packages
# Parameter: truck: a Truck object
#             end_time: the time that all deliveries should cease, in 'HH:MM' format
#
# Base Case: length of truck.payload[] = 0
# Space Time: O(N^2)
def deliver_packages(truck, end_time):

    # sets the time counter to the truck's designated start time, which is stored in truck.time
    time_counter = truck.time

    # if the start time is after the given end time, the function exits here and no packages are delivered
    if time_counter <= end_time:

        # sets the current location to the location id for the hub, which is 0
        current_location = 0

        # sets the status for all packages as 'In Transit' and logs the truck ID for each package
        for p in range(len(truck.payload)):

            package = package_hash.search(truck.payload[p].package_id)
            package.status = 'In Transit'
            package.truck_id = truck.id

        # the delivery algorithm continues as long as there are packages in the truck
        while len(truck.payload) > 0:

            # min_distance is set to a higher than possible value, so the first calculated distance will always be less
            # the values will be reset at the beginning of each iteration through the while loop
            min_distance = 9000.0
            package_index = None
            next_location = None

            # iterates through the list of packages to find the minimum distance to the next location
            # also logs the location id and the package index associated with that minimum distance
            for p in range(len(truck.payload)):
                package = truck.payload[p]
                if get_distance(current_location, address_lookup.get(package.address)) <= min_distance:
                    min_distance = get_distance(current_location, address_lookup.get(package.address))
                    next_location = address_lookup.get(package.address)
                    package_index = p

            # created variable for better readability
            delivered_package = (package_hash.search(truck.payload[package_index].package_id))

            # adds the calculated time for delivery to next location to the time counter.
            # if the time counter is greater than the end time, the loop is exited.
            # the current package is not delivered.
            time_counter += (min_distance/truck.mph)
            if time_counter > end_time:
                break

            # sets the new current location as the location of the package with the min_distance
            current_location = next_location
            # sets the time of delivery to the current time
            delivered_package.time_of_delivery = convert_float_time_to_hm(time_counter)
            # adds the minimum distance to the total truck mileage
            truck.mileage += min_distance
            # sets the package status as 'Delivered'
            delivered_package.status = 'Delivered'
            # removes the package from the truck's payload
            truck.payload.pop(package_index)

        # If all packages are delivered before the end time, the distance back to the hub is added to the mileage
        if time_counter <= end_time:
            truck.mileage += get_distance(current_location, 0)


# O(1): creates an instance of the hash table to store the packages
package_hash = HashTable()

# O(1): creates a dictionary to hold the address lookup table, in which the address is the key that is paired with its
# corresponding index in the distance table
address_lookup = {}

# O(1): creates the three truck objects that will deliver the packages
truck_1 = Truck()
truck_2 = Truck()
truck_3 = Truck()

# O(1): sets the ID number for the truck in question for better output readability
truck_1.id = 1
truck_2.id = 2
truck_3.id = 3

# O(N) instantiates the distance table from a csv file
distance_table = list(csv.reader(open('distance.csv', encoding='utf-8-sig')))

package_csv('packages.csv')
address_csv('address.csv')


# This class holds the main program and the console UI
class Main:
    def __init__(self):
        pass

    # O(1) sets the start time for each truck
    truck_1.time = convert_hm_time_to_float('08:00')
    truck_2.time = convert_hm_time_to_float('09:06')
    truck_3.time = convert_hm_time_to_float('10:30')

    # Each truck is loaded manually
    load_truck(truck_1, {1, 2, 8, 13, 14, 15, 16, 19, 20, 21, 27, 30, 34, 35, 39, 40})
    load_truck(truck_2, {3, 5, 6, 7, 12, 18, 25, 26, 29, 31, 32, 36, 37, 38})
    load_truck(truck_3, {4, 9, 10, 11, 17, 22, 23, 24, 28, 33})

    # updates the incorrect address for package 9.
    # The package is loaded on Truck 3 which does not leave until 10:30 AM.
    update_address(9, '410 S State St', 'Salt Lake City', 'UT', '84111')

    # converting the 'end time' - EOD - to a float
    end_time = convert_hm_time_to_float('23:59')

    deliver_packages(truck_1, end_time)
    deliver_packages(truck_2, end_time)
    deliver_packages(truck_3, end_time)

    print('Welcome to WGUPS package tracking')
    print('All deliveries were completed in ', "{0:.2f}".format(get_total_mileage(), 2), 'miles.')
    print('Please enter a number from the following menu')

    start = input(
            '1 - Package lookup \n2 - View status of all packages at a specific time \n0 - exit the program\n\n')

    if start == '1':
        p_id = input('Enter the package ID: ')

        # tests whether the input is an integer
        try:
            p_id = int(p_id)
        except:
            print('Only integer values are accepted')
            exit()

        # checks for a positive integer
        if p_id <= 0:
            print('Only positive values are accepted')
            exit()

        # prints an error if the package id is not in the hash table
        if package_hash.search(p_id) is None:
            print('Package not Found')
            exit()

        end_time = input('\nEnter a time in military time (HH:MM) between 00:00 and 24:00: ')

        # converts the input to a float. exits the program if the process fails
        try:
            end_time = convert_hm_time_to_float(end_time)
        except:
            print('Incorrect time format')
            exit()

        # checks if the time is in the proper range
        if not (0.0 <= end_time <= 24.0):
            print('Time out of range')
            exit()

        # reloading the trucks
        load_truck(truck_1, {1, 2, 8, 13, 14, 15, 16, 19, 20, 21, 27, 30, 34, 35, 39, 40})
        load_truck(truck_2, {3, 5, 6, 7, 12, 18, 25, 26, 29, 31, 32, 36, 37, 38})
        load_truck(truck_3, {4, 9, 10, 11, 17, 22, 23, 24, 28, 33})

        # Resets the package status and time of delivery
        for p in range(1, 41):
            package = package_hash.search(p)
            package.status = 'At Hub'
            package.time_of_delivery = ''

        # re-delivering packages
        deliver_packages(truck_1, end_time)
        deliver_packages(truck_2, end_time)
        deliver_packages(truck_3, end_time)

        # prints information for the given package
        print(package_hash.search(p_id))
        exit()

        # identical to the option above, except it doesn't ask for a specific package and the output is all packages
    if start == '2':
        end_time = input('Enter a time in military time (HH:MM) between 00:00 and 24:00: ')

        try:
            end_time = convert_hm_time_to_float(end_time)
        except:
            print('Incorrect time format')
            exit()

        if not (0.0 <= end_time <= 24.0):
            print('Time out of range')
            exit()

        load_truck(truck_1, {1, 2, 8, 13, 14, 15, 16, 19, 20, 21, 27, 30, 34, 35, 39, 40})
        load_truck(truck_2, {3, 5, 6, 7, 12, 18, 25, 26, 29, 31, 32, 36, 37, 38})
        load_truck(truck_3, {4, 9, 10, 11, 17, 22, 23, 24, 28, 33})

        for p in range(1, 41):
            package_hash.search(p).status = 'At Hub'
            package_hash.search(p).time_of_delivery = ''

        deliver_packages(truck_1, end_time)
        deliver_packages(truck_2, end_time)
        deliver_packages(truck_3, end_time)

        for p in range(1, 41):
            print(package_hash.search(p))

        exit()

    # checks for an invalid input
    if start not in ['1', '2', '0']:
        print('Incorrect selection\n')
        exit()

    print('Goodbye!')
    exit()

