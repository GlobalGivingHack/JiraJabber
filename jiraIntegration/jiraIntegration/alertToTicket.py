from Ticket import Ticket

def lambda_handler(event, context):
    return main(event, is_lambda=True)

def main(event, is_lambda=True):
    print 'in main for event {0}'.format(event)
    if event['action'] == 'create':
        return create(event['data'], is_lambda)
    elif event['action'] == 'update':
        pass
        #return update(event['data'], is_lambda)
    elif event['action'] == 'read':
        return read(event['data'], is_lambda)
    elif event['action'] == 'status_change':
        return status_change(event['data'], is_lambda)
    else:
        return False

def read(event, is_lambda):
    ticket = Ticket(event, is_lambda)
    return ticket.to_hash()

def status_change(event, is_lambda):
    ticket = Ticket(event, is_lambda)
    ticket.change_status("status")
    return ticket.to_hash()

def create(event, is_lambda):
    try:
        ticket = Ticket(event, is_lambda)
        print 'Creating new ticket'
        ticket.create()
        print 'created ticket with data: {0}'.format(vars(ticket))
        return ticket.to_hash()
        # TODO update_pager_duty_with_ticket_info()
    except Exception as e:
        print 'Error: {0}'.format(e)


if __name__ == '__main__':
    event = {
        'action': 'create',
        'data': {
            "subject": "45645"
        }
    }
    main(event, is_lambda=False)