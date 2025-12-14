from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.db import connection
from django.contrib.auth.decorators import login_required

@login_required
def lease4_list(request):
    sort_by = request.GET.get('sort', 'hostname')  # Default sort by hostname
    sort_order = request.GET.get('order', 'asc')   # Default order ascending
    order_direction = 'ASC' if sort_order == 'asc' else 'DESC'

    # Sanitize sort_by to prevent SQL injection (basic check for allowed columns)
    allowed_sort_columns = ['hostname', 'ipv4addr', 'hwaddr_formatted', 'subnet_id', 'expire']
    if sort_by not in allowed_sort_columns:
        sort_by = 'hostname' # Fallback to default if invalid

    # Map template column names to SQL column names (for sorting)
    sort_column_map = {
        'hostname': 'hostname',
        'ipv4addr': 'ipv4addr',
        'hwaddr_formatted': 'hwaddr_formatted', # Already formatted in SQL
        'subnet_id': 'subnet_id',
        'expire': 'expire',
    }
    sql_sort_column = sort_column_map.get(sort_by, 'hostname') # Default sort column

    with connection.cursor() as cursor:
        sql_query = f"""
            SELECT
                hostname,
                '0.0.0.0'::inet + address AS ipv4addr,
                colonseparatedhex(encode(hwaddr, 'hex'::text)) AS hwaddr_formatted,
                subnet_id,
                expire,
                address  -- Include the raw 'address' bigint for deletion
            FROM
                lease4
            ORDER BY
                {sql_sort_column} {order_direction}, hostname ASC -- Default secondary sort by hostname
        """ # Added f-string formatting for sort and direction

        cursor.execute(sql_query)
        columns = [col[0] for col in cursor.description]
        leases_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Pass sorting parameters to the template for creating sort links
    context = {
        'leases': leases_data,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }
    return render(request, 'lease4_list.html', context)

@login_required
def lease4_delete(request):
    if request.method == 'POST':
        address_to_delete = request.POST.get('address')
        if address_to_delete:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM lease4 WHERE address = %s", [address_to_delete])
                return redirect('lease4_list_url')
            except Exception as e:
                return HttpResponseBadRequest(f"Error deleting lease: {e}")
        else:
            return HttpResponseBadRequest("Lease address to delete not provided.")
    else:
        return HttpResponseBadRequest("Invalid request method for deletion.")
