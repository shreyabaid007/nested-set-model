from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

host = "127.0.0.1"
user = "root"
password = ""
db = "test"
con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
cur = con.cursor()
cur1 = con.cursor()


def getFullTree():
    cur.execute(" select * from NestedTree1")
    result = cur.fetchall()
    return result


def insertNode(right, part1):
    cur.execute("update NestedTree1 "
                "set  lft = CASE WHEN lft > " + right + " then lft+2 else lft end, "
                                                        "rgt = CASE WHEN rgt >= " + right + " then rgt+2 else rgt end "
                                                                                            "where rgt >= " + right + ";")
    cur.execute("insert into NestedTree1 (part,lft,rgt) value ('" + part1 + "'," + right + ", " + right + "+1);")


def getChildren(children):
    cur.execute("select * from Immediate_Subordinates1 where Mgrs='" + children + "' AND Mgrs <> Workers;")
    result = cur.fetchall()
    return result


def getParent(parent):
    cur.execute("select * from Immediate_Subordinates1 where Workers='" + parent + "' and Mgrs <> Workers;")
    result = cur.fetchall()
    return result


def getNode(part2):
    cur1.execute("select * from NestedTree1 where part='" + part2 + "' ;")
    result = cur1.fetchall()
    return result


@app.route('/')
def render_tree():
    res = getFullTree()
    return render_template('test.html', result=res, content_type='application/json')


@app.route('/', methods=['POST'])
def render_misc_tree():

    # fetching from form (frontend params)
    part1 = request.form['part1']
    part2 = request.form['part2']
    children = request.form['children']
    parent = request.form['parent']

    if request.form['hello_add']:
        result = getNode(part2)
        right = str(result[0].get("rgt"))

        # insert a new node in nested set model
        insertNode(right, part1)

    # get all the children (immediate subordinates)
    result1 = getChildren(children)
    res1 = result1 # redundant step

    # get immediate parent
    result2 = getParent(parent)
    res2 = result2

    # fetch full tree
    res = getFullTree()

    return render_template('test.html', result=res, result1=res1, result2=res2, content_type='application/json')


if __name__ == '__main__':
    app.run()
