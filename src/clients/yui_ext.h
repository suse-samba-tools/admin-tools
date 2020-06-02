#include "YEvent.h"
#include "YTable.h"
#include "YReplacePoint.h"
#include "YTree.h"
#include "YTreeItem.h"
#include <string.h>
#include <string>
using namespace std;

int YWidgetEvent_reason(YEvent *event);
YTable* dynamic_cast_YTable(YWidget * widget);
YReplacePoint* dynamic_cast_YReplacePoint(YWidget * widget);
YTree* dynamic_cast_YTree(YWidget * widget);
YTreeItem* YTree_currentItem(YWidget * widget);
void YTreeItem_setID(YTreeItem *item, string ID);
void YTableItem_setID(YTableItem *item, string ID);
void YItem_setID(YItem *item, string ID);
string YItem_getID(YItem *item);
string YTableItem_getID(YTableItem *item);
string YTreeItem_getID(YTreeItem *item);
