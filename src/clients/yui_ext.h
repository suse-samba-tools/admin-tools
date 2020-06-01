#include "YEvent.h"
#include "YTable.h"
#include <string.h>
#include <string>
using namespace std;

int YWidgetEvent_reason(YEvent *event);
YTable* dynamic_cast_YTable(YWidget * widget);
YReplacePoint* dynamic_cast_YReplacePoint(YWidget * widget);
