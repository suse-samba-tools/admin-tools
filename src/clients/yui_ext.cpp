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

YTreeItem* YTree_currentItem(YWidget * widget)
{
	YTree *w = dynamic_cast<YTree*>(widget);
	return w->currentItem();
}

void YTreeItem_setID(YTreeItem *item, string ID)
{
	YItem_setID((YItem*)item, ID);
}

string YTreeItem_getID(YTreeItem *item)
{
	return YItem_getID((YItem*)item);
}

void YTableItem_setID(YTableItem *item, string ID)
{
	YItem_setID((YItem*)item, ID);
}

string YTableItem_getID(YTableItem *item)
{
	return YItem_getID((YItem*)item);
}

void YItem_setID(YItem *item, string ID)
{
	char *cid = (char*)malloc(ID.size());
	memcpy(cid, ID.c_str(), ID.size());
	item->setData(cid);
}

string YItem_getID(YItem *item)
{
	return string((char*)item->data());
}
