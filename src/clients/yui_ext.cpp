#include "yui_ext.h"

int YWidgetEvent_reason(YEvent *event)
{
	YWidgetEvent *wevent =(YWidgetEvent*)event;
	return (int)wevent->reason();
}

YTable* dynamic_cast_YTable(YWidget * widget)
{
	return dynamic_cast<YTable*>(widget);
}

YReplacePoint* dynamic_cast_YReplacePoint(YWidget * widget)
{
	return dynamic_cast<YReplacePoint*>(widget);
}

YTree* dynamic_cast_YTree(YWidget * widget)
{
	return dynamic_cast<YTree*>(widget);
}
