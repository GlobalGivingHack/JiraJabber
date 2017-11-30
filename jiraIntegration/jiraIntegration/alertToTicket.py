from Ticket import Ticket
from PagerDuty import PagerDuty


def lambda_handler(event, context):
    main(event, is_lambda=True)

def main(event, is_lambda=True):
    print 'in main for event {0}'.format(event)
    try:
        ticket = Ticket(event, is_lambda)
        print 'Creating new ticket'
        ticket.create()
        # TODO update_pager_duty_with_ticket_info()
    except Exception as e:
        print 'Error: {0}'.format(e)


if __name__ == '__main__':
    event = {
        "subject": "45645"
    }
    main(event, is_lambda=False)