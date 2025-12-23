from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.db import connection
from django.contrib.auth.decorators import login_required

@login_required
def lease4_list(request):
    sort_by = request.GET.get('sort', 'hostname')
    sort_order = request.GET.get('order', 'asc')
    order_direction = 'ASC' if sort_order == 'asc' else 'DESC'

    allowed_sort_columns = ['hostname', 'hwaddr', 'ipv4', 'ipv6', 'subnet_id_v4', 'subnet_id_v6', 
                           'expire_v4', 'expire_v6', 'clientidv4', 'clientidv6', 
                           'valid_lifetime_v4', 'valid_lifetime_v6', 'state_v4', 'state_v6']
    if sort_by not in allowed_sort_columns:
        sort_by = 'hostname'

    sort_column_map = {col: col for col in allowed_sort_columns}
    sql_sort_column = sort_column_map.get(sort_by, 'hostname')

    with connection.cursor() as cursor:
        sql_query = f"""
            SELECT
                hostname,
                hwaddr,
                ipv4,
                ipv6,
                clientidv4,
                clientidv6,
                subnet_id_v4,
                subnet_id_v6,
                expire_v4,
                expire_v6,
                valid_lifetime_v4,
                valid_lifetime_v6,
                state_v4,
                state_v6,
                address_raw_v4,
                address_raw_v6
            FROM
                leaseview
            ORDER BY
                {sql_sort_column} {order_direction} NULLS LAST, hostname ASC
        """

        cursor.execute(sql_query)
        columns = [col[0] for col in cursor.description]
        leases_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {
        'leases': leases_data,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }
    return render(request, 'lease4_list.html', context)

@login_required
def lease4_delete(request):
    if request.method == 'POST':
        address_v4 = request.POST.get('address_v4')
        address_v6 = request.POST.get('address_v6')
        
        try:
            with connection.cursor() as cursor:
                if address_v4:
                    cursor.execute("DELETE FROM lease4 WHERE address = %s", [address_v4])
                if address_v6:
                    cursor.execute("DELETE FROM lease6 WHERE address = %s::inet", [address_v6])
            return redirect('lease4_list_url')
        except Exception as e:
            return HttpResponseBadRequest(f"Error deleting lease: {e}")
    else:
        return HttpResponseBadRequest("Invalid request method for deletion.")
