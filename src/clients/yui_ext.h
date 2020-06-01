#include "YEvent.h"
#include "YTable.h"
#include "YReplacePoint.h"
#include "YTree.h"
#include <string.h>
#include <string>
using namespace std;

int YWidgetEvent_reason(YEvent *event);
YTable* dynamic_cast_YTable(YWidget * widget);
YReplacePoint* dynamic_cast_YReplacePoint(YWidget * widget);
YTree* dynamic_cast_YTree(YWidget * widget);
