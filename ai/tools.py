from langchain.tools import tool

@tool
def search_iso(query: str):

    """Search ISO standards."""

    docs = retriever.invoke(query)

    return "\n\n".join(

        d.page_content

        for d in docs

    )
    
@tool
def get_asset(asset_id: int):

    asset = Asset.objects.get(

        pk=asset_id

    )

    return {

        "name":asset.asset_name,

        "category":asset.asset_category,

        "classification":asset.classification,

        "criticality":asset.asset_criticality,

        "confidentiality":asset.confidentiality_impact,

        "integrity":asset.integrity_impact,

        "availability":asset.availability_impact

    }