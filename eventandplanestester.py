import event as e
import planes as p

planes1 = [1,2,3,4]
planes2 = [3,4]

e1 = e.Event(1, 'reserve', 'ish', planes1)
e2 = e.Event(2, 'reserve', 'ish', planes1)
e3 = e.Event(1, 'reserve', 'ish', planes1)
e4 = e.Event(1, 'cancel', 'eth')
e5 = e.Event(1, 'reserve', 'ish', planes2)

print(e1)
print(e2)
print(e3)
print(e4)
print(e5)

assert not e1 == e2
assert e1.same(e2)
assert e2.same(e1)
assert e1 == e3
assert e1.same(e3)
assert not e1 == e4
assert not e1.same(e4)
assert not e1 == e5
assert not e1.same(e5)

print("All event asserts passed")
print()

airport = p.Planes()
#print(airport)

events = list()
#just one event
events.append(e1)
airport.fillPlane(events)
#print(airport)

#two events with the same person
events.append(e5)
airport.fillPlane(events)
print(airport)

planes3 = [7,8,9]
e6 = e.Event(1, 'reserve', 'eth', planes3)
events.append(e6)
airport.fillPlane(events)
print(airport)

print(airport.getView())
print(airport.getView())
print(airport.getView())

#canceling one of these events
e6 = e.Event(1, 'cancel', 'ish', planes1)
events.append(e6)
airport.fillPlane(events)
print(airport)

#a confilicting reservation


#canceling an event that doesn't exist
#events.append(e4)
#airport.fillPlane(events)
#print(airport)


planes3 = [7,8,9]
e6 = e.Event(1, 'cancel', 'eth', planes3)
events.append(e6)
airport.fillPlane(events)
print(airport)


#e6 = e.Event(1, 'reserve', 'eth', planes1)
#events.append(e6)
#airport.fillPlane(events)
#print(airport)

print(airport.getView())
